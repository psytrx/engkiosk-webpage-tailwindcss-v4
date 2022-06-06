from xml.sax.handler import feature_validation
import requests
import xml.etree.ElementTree as ET
import unicodedata
import re
import mimetypes
import datetime
import yaml
import html
from os.path import exists

from bs4 import BeautifulSoup as bs
from slugify import slugify
import frontmatter

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


CLEANR = re.compile('<.*?>')

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

    cleantext = re.sub(CLEANR, '', cleantext)
    return cleantext

def parse_headlines_from_html(raw_html):
    """
    We get HTML from the Podcast platforms Rich Text Editor.
    Often, this is not the best generated HTML, but yeah. Lets keep it for now.

    TODO Link sprungmarken
    """
    html = raw_html

    # Get all headlines
    headline_slugs = {}
    found_headlines = re.findall("<h3>(<span>)?(.*?)(</span>)?</h3>", html)
    for h in found_headlines:
        line = h[1]

        # Sometimes we match <br>
        # Here, we ensure to skip it
        if "<" in line and ">" in line:
            continue

        slug = slugify(line)
        #html = html.replace(f"<h3>{h}", f'<h3 class="mb-4 text-2xl md:text-3xl font-semibold text-coolGray-800" id="{slug}">{h}')
        html = html.replace(f"<h3>{h[0]}{h[1]}{h[2]}", f'<h3 id="{slug}">{line}')
        headline_slugs[slug] = line

    return html, headline_slugs

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


# Global variables
podcast_rss_feed = "https://feeds.redcircle.com/0ecfdfd7-fda1-4c3d-9515-476727f9df5e"
base_content_write_path = 'src/pages/podcast/episode'
base_image_write_path = 'public/images/podcast/episode'

# Get the XML Feed content
try:
    feed_response = requests.get(podcast_rss_feed)
    feed_response.raise_for_status()

    # Catching this exception is enough, because this is the
    # parent exceptions for Connection, Timeouts, Redirect and HTTP errors.
    # See https://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
except requests.exceptions.RequestException as e:
    raise SystemExit(e)

# requests makes an educated guess on the response encoding.
# Here we overwrite the encoding to UTF-8
feed_response.encoding = 'utf-8'

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

    # Get all headlines from description and add
    # jump markers to <h[1-6]> tags
    html_content, headlines = parse_headlines_from_html(description)
    description_html = html_content

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
    headline_info = '||'.join([f'{slug}::{headline}' for slug, headline in headlines.items()])

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
        image_filename = f"{base_image_write_path}/{image_filename}"
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

    full_file_path = f'{base_content_write_path}/{filename}'

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