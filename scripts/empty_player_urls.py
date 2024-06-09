import logging
import sys

from episode_finder import EpisodeFinder
from constants import EPISODES_STORAGE_DIR
from functions import (
    build_correct_file_path,
    configure_global_logger
)


def find_empty_player_urls(path_md_files) -> int:
    """
    Iterating through all Podcast Episodes data files and check
    if the player links for Spotify, Amazon Music and so on
    are filled properly.

    If a player link is missing, it will output this file.
    If an empty response is provided, everything is fine.
    Just remember: On Unix systems, no news are good news.
    """
    exit_code = 0

    # Get existing podcast episodes
    episode_finder = EpisodeFinder()
    episode_finder.load_episodes_from_storage(path_md_files)
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
            # Do we have a value for the player key?
            if not val:
                missing.append(key)

        if missing:
            missing_urls = ", ".join(missing)
            logging.error(f"Episode {file_path} is missing player URLs for {missing_urls}")

            exit_code = 1

    return exit_code


if __name__ == "__main__":
    # Setup logger
    configure_global_logger()

    exit_code = find_empty_player_urls(
        build_correct_file_path(EPISODES_STORAGE_DIR)
    )
    sys.exit(exit_code)