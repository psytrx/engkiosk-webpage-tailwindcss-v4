import os
from os.path import isfile, join
import re

from episode import (
    Episode
)

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
            episode_object = Episode(episode_file_path)

            # Frontmatter by episode filename
            self.__episodes_by_filename[episode_file_path] = episode_object

            # Frontmatter by episode number
            episode_number = self.get_episode_number_from_filename(episode_file_path)
            self.__episodes_by_number[episode_number] = episode_object
    
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
        episode_number = self.__trim_episode_number(episode_number)

        return episode_number

    def __trim_episode_number(self, episode_number):
        """
        Trims the episode number to remove leading zeros.
        """
        if episode_number.startswith("0"):
            episode_number = episode_number[len("0"):]

        return episode_number

    def get_podcast_episode_by_number(self, number):
        """
        Gets the podcast episode data by number.

        {number} is the number of the podcast.

        If the episode was found, the episode object is returned.
        If not, None is returned.
        """
        number = self.__trim_episode_number(number)
        if number not in self.__episodes_by_number:
            return None

        return self.__episodes_by_number[number]
