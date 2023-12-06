import os
from os.path import isfile, join
import logging
import sys

# External libraries
import frontmatter

# Global variables
PATH_MARKDOWN_FILES = 'src/content/podcast'


def find_empty_player_urls(path_md_files) -> int:
    """
    Going through all Podcast Episode Markdown files and checks
    if the player links for Spotify, Amazon Music and so on
    are set properly.

    If a player link is missing, it will output this file.
    If an empty response is provided, everything is fine.
    Just remember: No news are good news.
    """
    exit_code = 0

    # Get existing podcast episodes
    episodes = [f for f in os.listdir(path_md_files) if isfile(join(path_md_files, f)) and f.endswith('.md')]
    for episode in episodes:
        file_path = f"{path_md_files}/{episode}"
        with open(file_path) as f:
            episode = frontmatter.load(f)
            keys_to_check = [
                'spotify',
                'google_podcasts',
                'apple_podcasts',
                'amazon_music',
                'deezer',
                'youtube'
            ]
            missing = []
            for key in keys_to_check:
                val = episode.get(key)
                if not val:
                    missing.append(key)

            if missing:
                missing_urls = ", ".join(missing)
                logging.error(f"Episode {file_path} is missing player URLs for {missing_urls}")

                exit_code = 1

    return exit_code


if __name__ == "__main__":
    # Setup logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    p = PATH_MARKDOWN_FILES

    # Determine if the script is called from root
    # or from the scripts directory.
    directory_path = os.getcwd()
    folder_name = os.path.basename(directory_path)
    if folder_name == "scripts":
        p = f"../{PATH_MARKDOWN_FILES}"

    exit_code = find_empty_player_urls(p)
    sys.exit(exit_code)