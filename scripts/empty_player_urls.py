import logging
import sys

from episode_finder import (
    EpisodeFinder
)

from functions import (
    build_correct_file_path
)

from pathes import (
    EPISODES_STORAGE_DIR
)

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
    episode_finder = EpisodeFinder(path_md_files)
    episodes = episode_finder.get_episodes()
    for file_path, episode in episodes.items():
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

    file_path = build_correct_file_path(EPISODES_STORAGE_DIR)
    exit_code = find_empty_player_urls(file_path)
    sys.exit(exit_code)