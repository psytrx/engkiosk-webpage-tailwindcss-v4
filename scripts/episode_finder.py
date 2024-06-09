import os
from os.path import isfile, join

from episode import (
    Episode
)

class EpisodeFinder:
    def __init__(self):
        self.__episodes_by_filename = {}
        self.__episodes_by_number = {}

    def load_episodes_from_storage(self, episode_storage_path):
        """
        Load all episodes from the storage directory.
        Loading in this context means to read the frontmatter and store it in a dictionary.
        We store the frontmatter by filename and by episode number.
        """
        episodes = [f for f in os.listdir(episode_storage_path) if isfile(join(episode_storage_path, f)) and f.endswith('.md')]
        for episode in episodes:
            episode_file_path = os.path.join(episode_storage_path, episode)
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

    def get_episode_number_from_filename(self, filename, leading_zero=False):
        """
        Retrieves the episode number from the episode filename.
        A podcast episode filename is like `94-die-realität-des-freelancings-zwischen-selbstbestimmung-und-unsicherheit-mit-index-out-of-bounds.md`
        In the example, 94 is the episode number.

        Input: ../src/content/podcast/04-lohnt-der-einstieg-in-open-source.md
        Output (leading_zero=False): 4
        Output (leading_zero=True): 04

        Input: ../src/content/podcast/12-make-oder-buy.md
        Output: 12
        """
        index = filename.find('-')

        # We have one episode which starts with '-1'
        # If we search for '-', we get the minus sign.
        # Hence we need to skip it.
        if index == 0:
            index = filename[1:len(filename)].find('-')
            episode_number = filename[0:index+1]

        else:
            episode_number = filename[0:index]

        if not leading_zero:
            episode_number = self.__trim_episode_number(episode_number)
        else:
            episode_number = episode_number.zfill(2)

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
