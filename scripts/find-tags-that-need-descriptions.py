import json
import os
from os.path import isfile, join
import sys

import frontmatter

# Global variables
PODCAST_CONTENT_FILES = '../src/pages/podcast/episode'
BLOGPOST_CONTENT_FILES = '../src/pages/blog/post'
TAG_FILE = '../src/data/tags.json'


def read_all_tags_from_content_files(pathes):
    tags = set(())
    for p in pathes:
        # Get existing podcast episodes
        content_files = [f for f in os.listdir(p) if isfile(join(p, f)) and f.endswith('.md')]
        for content_file in content_files:
            full_file_path = f'{p}/{content_file}'

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
    for tag_name, tag_description in tag_descriptions.items():
        if tag_description:
            tags_with_description.add(tag_name)
        else:
            tags_without_descriptions.add(tag_name)

    # Checking for new tags
    for tag_name in tags:
        if tag_name not in tags_with_description and tag_name not in tags_without_descriptions:
            tags_without_descriptions.add(tag_name)

    return tags_without_descriptions


if __name__ == "__main__":
    content_pathes = [
        PODCAST_CONTENT_FILES,
        BLOGPOST_CONTENT_FILES,
    ]
    tags = read_all_tags_from_content_files(content_pathes)
    tag_descriptions = read_tag_descriptions(TAG_FILE)
    tags = get_all_tags_without_description(tag_descriptions, tags)

    for t in tags:
        print(t)

    if len(tags):
        sys.exit(1)

    sys.exit(0)