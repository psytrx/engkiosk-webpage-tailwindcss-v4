from xml.sax.handler import feature_validation
import requests
import xml.etree.ElementTree as ET
import unicodedata
import re
import mimetypes
import datetime


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

    # Date format: Tue, 05 Apr 2022 04:25:00 +0000
    pub_date = item.find('pubDate').text
    # See full list of format codes here
    # https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
    date_parsed = datetime.datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d')
    
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

    content = (
        '---\n'
        'layout: ../../layouts/post.astro\n'
        f'title: "{title}"\n'
        # TODO Do we need tags?
        f'tag: movie\n'
        f'date: {date_parsed}\n'
        f'image: {image_filename}\n'
        # TODO Do we need author?
        f'author: don\n'
        # TODO What would be useful as a short description?
        f'description: Which Treats of the Character and Pursuits of the Famous Gentleman Don Quixote of La Mancha\n'
        '---\n'
        '\n'
        # TODO Description has tons of HTML code right now
        f'{description}'
    )

    # Write file to disk as a new podcast episode
    f = open(f'{base_content_write_path}/{filename}', 'w')
    f.write(content)
    f.close()