import argparse
import json
import os
from os.path import isfile, join
import sys
import logging

import frontmatter

# Global variables
PODCAST_CONTENT_FILES = 'src/pages/podcast/episode'
BLOGPOST_CONTENT_FILES = 'src/pages/blog/post'
TAG_FILE = 'src/data/tags.json'


def read_all_tags_from_content_files(pathes):
    tags = set(())
    for p in pathes:
        logging.info(f"Reading tags from files in {p} ...")
        # Get existing podcast episodes
        content_files = [f for f in os.listdir(p) if isfile(join(p, f)) and f.endswith('.md')]
        for content_file in content_files:
            full_file_path = f'{p}/{content_file}'
            logging.info(f"Processing file {full_file_path} ...")

            with open(full_file_path) as f:
                fm = frontmatter.load(f)
                frontmatter_tags = fm.get("tags")

                for tag in frontmatter_tags:
                    tags.add(tag)

    return tags


def read_tag_descriptions(tag_file):
    with open(tag_file) as f:
        data = json.load(f)

    return data

def get_all_tags_without_description(tag_descriptions, tags):
    tags_with_description = set(())
    tags_without_descriptions = set(())

    # Collecting tags that are already part of the tag file
    for tag_name, tag_descriptions in tag_descriptions.items():
        # If one of the keys don't exist
        if "short_desc" not in tag_descriptions or "long_desc" not in tag_descriptions:
            tags_without_descriptions.add(tag_name)
            continue

        # If both keys exists and are filled
        if ("short_desc" in tag_descriptions and tag_descriptions['short_desc']) \
            and ("long_desc" in tag_descriptions and tag_descriptions['long_desc']):
            tags_with_description.add(tag_name)
            continue

        tags_without_descriptions.add(tag_name)

    # Checking for new tags
    for tag_name in tags:
        if tag_name not in tags_with_description and tag_name not in tags_without_descriptions:
            tags_without_descriptions.add(tag_name)

    return tags_without_descriptions


if __name__ == "__main__":
    # Argument and parameter parsing
    cli_parser = argparse.ArgumentParser(description='Find tags without descriptions. Without `-write-file`, the tags get printed to stdout.')
    cli_parser.add_argument(
        '-write-file',
        action='store_true',
        help='Modifies the local tag storage file and adds missing tags (default: %(default)s)')

    args = cli_parser.parse_args()

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

    content_pathes = [
        f"{folder_prefix}{PODCAST_CONTENT_FILES}",
        f"{folder_prefix}{BLOGPOST_CONTENT_FILES}",
    ]
    TAG_FILE_PATH = f"{folder_prefix}{TAG_FILE}"

    tags = read_all_tags_from_content_files(content_pathes)
    len_content_tags = len(tags)
    logging.info(f"Reading existing tag descriptions from {TAG_FILE_PATH} ...")
    tag_descriptions = read_tag_descriptions(TAG_FILE_PATH)
    logging.info(f"Determining tags with missing descriptions out of {len_content_tags} unique content tags ...")
    tags = get_all_tags_without_description(tag_descriptions, tags)
    logging.info(f"Found {len(tags)} tags with missing descriptions out of {len_content_tags} unique content tags ...")

    # Should we print out the files?
    if not args.write_file:
        for t in tags:
            print(t)

        # We let it fail, because in a perfect world, there should be
        # no missing descriptions. However, if we let this run as a CI
        # job, the CI job failure pings us to take action.
        if len(tags):
            sys.exit(1)

    logging.info(f"Writing missing tag structures into file {TAG_FILE_PATH} ...")
    # Write the missing tags to the local tag file
    for t in tags:
        # If the tag already exists, mostly a subkey is missing
        if t not in tag_descriptions:
            tag_descriptions[t] = {}

        subKeys = ["short_desc", "long_desc"]
        for k in subKeys:
            if k not in tag_descriptions[t]:
                tag_descriptions[t][k] = ""

    with open(TAG_FILE_PATH, 'w') as fp:
        json.dump(tag_descriptions, fp, indent=4)

    logging.info(f"Writing missing tag structures into file {TAG_FILE_PATH} ... done")

    sys.exit(0)
