from xml.sax.handler import feature_validation
import requests
import xml.etree.ElementTree as ET

podcast_rss_feed = "https://feeds.redcircle.com/0ecfdfd7-fda1-4c3d-9515-476727f9df5e"

try:
    feed_response = requests.get(podcast_rss_feed)

    # Catching this exception is enough, because this is the
    # parent exceptions for Connection, Timeouts, Redirect and HTTP errors.
    # See https://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
except requests.exceptions.RequestException as e:
    raise SystemExit(e)

parsed_xml = ET.fromstring(feed_response.text)
channel = parsed_xml.find("channel")

# Get all episodes
for item in channel.findall('item'):
    # Other fields that are available
    # - itunes:episodeType
    # - itunes:title
    # - itunes:episode
    # - itunes:author
    # - content:encoded
    # - itunes:duration
    title = item.find('title')
    description = item.find('description')
    link = item.find('link')

    # TODO parse pubDate into date object
    # Tue, 05 Apr 2022 04:25:00 +0000
    pubDate = item.find('pubDate')
    
    image = item.find('{http://www.itunes.com/dtds/podcast-1.0.dtd}image')
    if image is not None:
        image = image.attrib.get('href')
    else:
        image = ""

    print(title.text)