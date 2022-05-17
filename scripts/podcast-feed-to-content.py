from xml.sax.handler import feature_validation
import requests
import xml.etree.ElementTree as ET
import unicodedata
import re
import mimetypes
import datetime
import sys
import yaml
import html
from slugify import slugify

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
    cleantext = re.sub(CLEANR, '', raw_html)
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
        html = html.replace(f"<h3>{h}", f'<h3 class="mb-4 text-2xl md:text-3xl font-semibold text-coolGray-800" id={slug}>{h}')
        headline_slugs[slug] = h

    # For some unknown reason, the tailwind classes don't work here
    # I have to go with inline styles ...
    html = html.replace("<ul>", '<ul class="list-disc px-5 mb-6 md:px-5 text-base md:text-lg text-coolGray-500" style="list-style-type: disc;">')
    html = html.replace("<li><span>", '<li>')
    html = html.replace("</span></li>", "</li>")

    # Style links
    # Again, no clue why the default styles overrule
    # TODO Figure out why style is necessary, and hover is not working
    html = html.replace('<a ', '<a class="underline hover:no-underline" style="text-decoration-line: underline;"')

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
        # In line with chaptermarks from podcast player
        # See https://github.com/podigee/podigee-podcast-player/blob/master/docs/configuration.md
        entry = {
            "start": c[0],
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

    # If you use a standing desk, it might be good, if you take a seat now.
    # The next line is pretty dirty, even it is called to be beautiful.
    # ... <waiting until you sit> ...
    # Now jump to the function documentation to see why it is far from beautiful.
    html_info = make_html_beautiful(description)
    description_html = html_info["html"]

    chapter = get_chapter_from_description(description)

    # Parse headlines
    headline_info = '||'.join([f'{slug}::{headline}' for slug, headline in html_info["headlines"].items()])

    description_text_only = remove_html_tags(description)

    ix = max(description_text_only.find(' ', 120), 120)
    description_short = description_text_only[:ix]

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
    }
    content_yaml = yaml.dump(data)

    content = (
        '---\n'
        f'{content_yaml}\n'
        '---\n'
        '\n'
        f'{description_html}'
    )

    # Write file to disk as a new podcast episode
    f = open(f'{base_content_write_path}/{filename}', 'w', encoding='utf8')
    f.write(content)
    f.close()