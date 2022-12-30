from datetime import datetime
import os
import logging
import json
import xml.etree.cElementTree as ET

#
# Builds an OPML file based on our podcasts.
# Docs: http://opml.org/
#

# Global variables
PODCAST_JSON_FILE = 'src/data/german-tech-podcasts.json'
STORAGE = "public/deutsche-tech-podcasts/podcasts.opml"


def generate_opml_file(merged_json_file_path, storage_path):
    opml = ET.Element("opml", version="2.0")
    head = ET.SubElement(opml, "head")

    ET.SubElement(head, "title").text = "Deutschsprachige Tech Podcasts"
    ET.SubElement(head, "dateCreated").text = datetime.now().isoformat()
    ET.SubElement(head, "ownerName").text = "Engineering Kiosk"
    ET.SubElement(head, "ownerEmail").text = "stehtisch@engineeringkiosk.dev"

    body = ET.SubElement(opml, "body")
    
    logging.info(f"Reading merged JSON file {merged_json_file_path} ...")
    with open(merged_json_file_path) as f:
        data = json.load(f)

        # Sort by name
        sorted_data = sorted(data, key=lambda x: x['name'].lower())
        for podcast in sorted_data:
            ET.SubElement(body, "outline", title=podcast["name"], text=podcast["name"], type="rss", xmlUrl=podcast["rssFeed"], htmlUrl=podcast["website"])

    tree = ET.ElementTree(opml)
    ET.indent(tree, space="\t", level=0)
    tree.write(storage_path, xml_declaration=True, encoding='utf-8')

    logging.info("Aaaaand we are done")


if __name__ == "__main__":
    # Setup logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    # Determine if the script is called from root
    # or from the scripts directory.
    directory_path = os.getcwd()
    folder_name = os.path.basename(directory_path)
    folder_prefix = ""
    if folder_name == "scripts":
        folder_prefix = "../"

    merged_json_file_path = f"{folder_prefix}{PODCAST_JSON_FILE}"
    storage_path = f"{folder_prefix}{STORAGE}"

    generate_opml_file(merged_json_file_path, storage_path)