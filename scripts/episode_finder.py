import os
from os.path import isfile, join
import re

# External libraries
import frontmatter

class EpisodeFinder:
    def __init__(self, episode_storage_path):
        self.__episode_number_regex = re.compile('([-\d]*)-')
        self.__episode_storage_path = episode_storage_path
        self.__episodes_by_filename = {}
        self.__episodes_by_number = {}
        
        self.load_episodes_from_storage()

    def load_episodes_from_storage(self):
        """
        Load all episodes from the storage directory.
        Loading in this context means to read the frontmatter and store it in a dictionary.
        We store the frontmatter by filename and by episode number.
        """
        episodes = [f for f in os.listdir(self.__episode_storage_path) if isfile(join(self.__episode_storage_path, f)) and f.endswith('.md')]
        for episode in episodes:
            episode_file_path = os.path.join(self.__episode_storage_path, episode)
            with open(episode_file_path) as f:
                episode_frontmatter = frontmatter.load(f)

            # Frontmatter by episode filename
            self.__episodes_by_filename[episode_file_path] = episode_frontmatter

            # Frontmatter by episode number
            episode_number = self.get_episode_number_from_filename(episode_file_path)
            self.__episodes_by_number[episode_number] = episode_frontmatter
    
    def get_episodes(self):
        """
        Get all episodes by filename.
        """
        return self.__episodes_by_filename

    # If we have a number like 00 or 05, remove the first 0
    def get_episode_number_from_filename(self, filename):
        """
        Get the episode number from the filename.

        Input: ../src/content/podcast/04-lohnt-der-einstieg-in-open-source.md
        Output: 4

        Input: ../src/content/podcast/12-make-oder-buy.md
        Output: 12
        """
        episode_number = re.findall(self.__episode_number_regex, filename)[0]

        if episode_number.startswith("0"):
            episode_number = episode_number[len("0"):]

        return episode_number