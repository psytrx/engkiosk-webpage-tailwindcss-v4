from xml.sax.handler import feature_validation
import argparse
import requests
import xml.etree.ElementTree as ET
import unicodedata
import re
import mimetypes
import datetime
import yaml
import html
import toml
from os.path import exists, isfile, join
from os import listdir
import logging

# External libraries
from bs4 import BeautifulSoup as bs
from slugify import slugify
import frontmatter

# Global variables
PODCAST_RSS_FEED = "https://feeds.redcircle.com/0ecfdfd7-fda1-4c3d-9515-476727f9df5e"
PATH_MARKDOWN_FILES = 'src/pages/podcast/episode'
PATH_IMAGE_FILES = 'public/images/podcast/episode'
TOML_FILE = 'netlify.toml'
REDIRECT_PREFIX = '/episodes/'

# From the Django project
# See https://docs.djangoproject.com/en/2.1/_modules/django/utils/text/#slugify
def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


def download_file(url, local_filename):
    """
    Downloads {url} and stores it into {local_filename}.
    Original file extension will be guessed based on the mime type.

    Returns the full local file name incl. file extension.

    Exceptions are bubbled up, once raised.
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        # Determine file extension
        content_type = r.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
        file_name = f'{local_filename}{extension}'

        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return file_name


# Not an awesome logic, but enough for our usecase.
# See https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string for more.
def remove_html_tags(raw_html):
    """
    Removing all HTML tags.
    """
    # First we replace "</p>" with "</p> " (adding a single whitespace).
    # Primarily to ensure that after the removal of each HTML element, 
    # we have a whitespace at the end of each sentence/paragraph.
    # Otherwise, our text would look like
    #
    #   [...] im Engineering Kiosk.Indirekt knüpfen [...]
    #
    # Take attention to the missing whitespace between the sentences
    cleantext = raw_html.replace("</p>", "</p> ")

    html_tags_regex = re.compile('<.*?>')
    cleantext = re.sub(html_tags_regex, '', cleantext)
    return cleantext


def make_html_beautiful(raw_html):
    """
    Okay. Welcome to the real dirty part.
    The thing is ... we get HTML form the Podcast platforms Rich Text Editor.
    And we want to have a nice looking presentation of this content on
    our webpage.
    We can do some highly intelligent computer science logic or play dirty, simple
    and full of potential errors, edge cases and more.
    And that is what we are doing ....

        Welcome to HTML string replacing

    We can do it either here or in the JavaScript of the static site generator.
    For now, I decided to do it here. And yes, this means, if we change the design
    of our webpage, we have to edit this one here.
    Bad, but to be honest, this design won't likely change in the next 2 years.

    If you think this is way to dirty for a Software Engineering Podcast and you feel
    challenged, go ahead, improve it and send us a PR. Happy to review it.
    Otherwise, we continue with this crime.

    TODO Link sprungmarken
    """
    html = raw_html.replace("<p><span>", '<p class="mb-6 text-base md:text-lg text-coolGray-500">')
    html = html.replace("</span></p>", "</p>")

    html = html.replace("<p><br></p>", "")

    html = html.replace("<p>", '<p class="mb-6 text-base md:text-lg text-coolGray-500">')

    # Headlines
    html = html.replace("<h3><br></h3>", "")
    html = html.replace("<h3><span>", '<h3>')
    html = html.replace("</span></h3>", "</h3>")

    # Get all headlines
    headline_slugs = {}
    found_headlines = re.findall("<h3>(.*?)</h3>", html)
    for h in found_headlines:
        slug = slugify(h)
        html = html.replace(f"<h3>{h}", f'<h3 class="mb-4 text-2xl md:text-3xl font-semibold text-coolGray-800" id="{slug}">{h}')
        headline_slugs[slug] = h

    html = html.replace("<ul>", '<ul class="list-disc px-5 mb-6 md:px-5 text-base md:text-lg text-coolGray-500">')
    html = html.replace("<li><span>", '<li class="mb-3">')
    html = html.replace("<li>", '<li class="mb-3">')

    html = html.replace("</span></li>", "</li>")

    html = html.replace("<span>", '')
    html = html.replace("</span>", '')

    html = html.replace('<a ', '<a class="underline hover:no-underline" ')

    # This is also very dirty
    # We need the headline <-> slug relation.
    # We could write another function, but we have the whole processing
    # already here. So why not?
    info = {
        "html": html,
        "headlines": headline_slugs,
    }
    return info


def get_chapter_from_description(description):
    # Chapter entries look like
    #       <p><span>(00:00:00) Intro</span></p>
    found_chapters = re.findall("<p><span>\(([0-9:]*)\) ([^<]*)</span></p>", description)
    if len(found_chapters) == 0:
        found_chapters = re.findall("<p>\(([0-9:]*)\) ([^<]*)</p>", description)

    chapter = []
    for c in found_chapters:
        start_time = c[0]
        if start_time.count(":") == 1:
            start_time = f"00:{start_time}"

        # In line with chaptermarks from podcast player
        # See https://github.com/podigee/podigee-podcast-player/blob/master/docs/configuration.md
        entry = {
            "start": start_time,
            "title": html.unescape(c[1]),
        }
        chapter.append(entry)

    return chapter


def sync_podcast_episodes(rss_feed, path_md_files, path_img_files):
    """
    Syncs the Podcast Episodes from the RSS feed down to disk
    and prepares the content to match the structure of the used
    static site generator.

    This means in detail:
    - Read the RSS feed
    - Extracts the information into a Frontmatter structure
    - Downloads the image
    - Writes a Markdown and image file to disk

    """

    logging.info(f"Reading Podcast RSS Feed {rss_feed} ...")
    # Get the XML Feed content
    try:
        feed_response = requests.get(rss_feed)
        feed_response.raise_for_status()

        # Catching this exception is enough, because this is the
        # parent exceptions for Connection, Timeouts, Redirect and HTTP errors.
        # See https://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    logging.info(f"Reading Podcast RSS Feed {rss_feed} ... Successful")

    # requests makes an educated guess on the response encoding.
    # Here we overwrite the encoding to UTF-8
    feed_response.encoding = 'utf-8'

    logging.info("Processing Podcast Episode items ...")

    # Parse the XML and process all items
    parsed_xml = ET.fromstring(feed_response.text)
    channel = parsed_xml.find("channel")
    for item in channel.findall('item'):
        # Other fields that are available
        # - itunes:episodeType
        # - itunes:title
        # - itunes:episode
        # - itunes:author
        # - content:encoded
        # - itunes:duration
        # - link
        title = item.find('title').text
        description = item.find('description').text

        # If you use a standing desk, it might be good, if you take a seat now.
        # The next line is pretty dirty, even it is called to be beautiful.
        # ... <waiting until you sit> ...
        # Now jump to the function documentation to see why it is far from beautiful.
        html_info = make_html_beautiful(description)
        description_html = html_info["html"]

        # Pretty print html to make it somehow
        # human debuggable.
        soup = bs(description_html, features="lxml")
        prettyHtml = soup.prettify()

        # Remove <html> and <body> tags
        prettyHtml = prettyHtml.replace("<html>", "")
        prettyHtml = prettyHtml.replace("<body>", "")
        prettyHtml = prettyHtml.replace("</body>", "")
        prettyHtml = prettyHtml.replace("</html>", "")
        prettyHtml = prettyHtml.strip()

        chapter = get_chapter_from_description(description)

        # Parse headlines
        headline_info = '||'.join([f'{slug}::{headline}' for slug, headline in html_info["headlines"].items()])

        description_text_only = remove_html_tags(description)

        ix = max(description_text_only.find(' ', 120), 120)
        description_short = description_text_only[:ix]
        description_short += " ..."

        # Date format: Tue, 05 Apr 2022 04:25:00 +0000
        pub_date = item.find('pubDate').text
        # See full list of format codes here
        # https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        date_parsed = datetime.datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d')

        mp3 = item.find('enclosure')
        mp3_link = mp3.attrib.get('url')

        # If an image is available,
        # download it and store it in the public folder
        image = item.find('{http://www.itunes.com/dtds/podcast-1.0.dtd}image')
        if image is not None:
            image = image.attrib.get('href')
            image_filename = slugify(title, True)
            # File extension will be determined in download_file
            image_filename = f"{path_img_files}/{image_filename}"
            image_filename = download_file(image, image_filename)

            # Remove prefix "public"
            prefix = "public"
            image_filename = image_filename[len(prefix):]

        else:
            image = ""

        # Build the filename and the content
        filename = slugify(title, True)
        filename = f'{filename}.md'

        data = {
            'layout': '../../../layouts/podcast-episode.astro',
            'title': title,
            'audio': mp3_link,
            'date': date_parsed,
            'image': image_filename,
            'description': description_short,
            'headlines': headline_info,
            'chapter': chapter,
            'spotify': '',
            'google_podcasts': '',
            'apple_podcasts': '',
            'amazon_music': ''
        }

        full_file_path = f'{path_md_files}/{filename}'

        # If the file exists, we want to read the frontmatter, extract
        # the spotify, google podcasts, etc. links and write this to the
        # new data.
        # Why? Because the Podcast player links are added manual.
        # The rest of the data (title, description, etc.) are parsed
        # out of the RSS feed and maintained in a different application.
        # This way, we "update" our local data based on the management application,
        # but keep the manual parts.
        if exists(full_file_path):
            with open(full_file_path) as f:
                episode = frontmatter.load(f)

                keys_to_keep = [
                    'spotify',
                    'google_podcasts',
                    'apple_podcasts',
                    'amazon_music'
                ]
                for key in keys_to_keep:
                    val = episode.get(key)
                    if val:
                        data[key] = episode.get(key)

        content_yaml = yaml.dump(data)
        content = (
            '---\n'
            f'{content_yaml}\n'
            '---\n'
            '\n'
            f'{prettyHtml}'
        )

        # Write file to disk as a new podcast episode
        f = open(full_file_path, 'w', encoding='utf8')
        f.write(content)
        f.close()

    logging.info("Processing Podcast Episode items ... Successful")


def trim_prefix(line, prefix):
    """
    Removes prefix from line.
    """
    if line.startswith(prefix):
        line = line[len(prefix):]

    return line


def create_redirects(file_to_parse, path_md_files, redirect_prefix):
    """
    Creates redirects for every Podcast episode to /episodes/123 by

    1. Reading the toml file
    2. Processing all podcast episodes
    3. Writing the toml file
    """
    # Read existing toml file
    parsed_toml = ""
    with open(file_to_parse) as f:
        content = f.read()
        parsed_toml = toml.loads(s=content)

    # Restructure existing redirects into a hashmap
    # for easier lookup
    redirect_episode_number_regex = re.compile(f"{redirect_prefix}([0-9]*)$")
    redirect_map = {}
    for redirect in parsed_toml['redirects']:
        # Find the number of the episode
        redirect_episode_number = re.findall(redirect_episode_number_regex, redirect["from"])[0]
        if redirect_episode_number == "":
            continue

        redirect_map[redirect_episode_number] = redirect


    # Get existing podcast episodes
    episodes = [f for f in listdir(path_md_files) if isfile(join(path_md_files, f)) and f.endswith('.md')]

    episode_number_regex = re.compile('([0-9]*)-')
    for episode in episodes:
        # Find the number of the episode
        episode_number = re.findall(episode_number_regex, episode)[0]

        # If we have a number loke 00 or 05, remove the first 0
        episode_number = trim_prefix(episode_number, "0")

        # Check if we have a redirect for this episode already
        # If yes, skip ip
        if episode_number in redirect_map:
            logging.info(f"Skipping redirect processing for episode {episode_number}: Redirect exists already.")
            continue

        logging.info(f"Adding redirect for episode {episode_number}")

        episode_file = episode.removesuffix(".md")
        new_redirect = {
            "from": f"/episodes/{episode_number}",
            "to": f"/podcast/episode/{episode_file}?pk_campaign=shortlink",
            "status": 301,
            "force": True,
        }

        parsed_toml['redirects'].append(new_redirect)

    # Write new file
    with open(file_to_parse, 'w') as f:
        toml.dump(o=parsed_toml, f=f)


if __name__ == "__main__":
    # Argument and parameter parsing
    cli_parser = argparse.ArgumentParser(description='Automate new Podcast Episide parsing')
    # See https://stackoverflow.com/questions/40324356/python-argparse-choices-with-a-default-choice
    cli_parser.add_argument('Mode',
        metavar='mode',
        type=str,
        default='sync',
        const='sync',
        nargs='?',
        choices=['sync', 'redirect'],
        help='Mode to execute. Supported: sync, redirect (default: %(default)s)')

    args = cli_parser.parse_args()

    # Setup logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    match args.Mode:
        case "sync":
            sync_podcast_episodes(PODCAST_RSS_FEED, PATH_MARKDOWN_FILES, PATH_IMAGE_FILES)
        case "redirect":
            # TODO Once Python 3.11 is out, replace toml library with stdlib
            # See https://peps.python.org/pep-0680/
            create_redirects(TOML_FILE, PATH_MARKDOWN_FILES, REDIRECT_PREFIX)