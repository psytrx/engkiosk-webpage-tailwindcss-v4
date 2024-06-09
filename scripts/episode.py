import os
import ntpath

from functions import build_correct_file_path
from constants import TRANSCRIPT_STORAGE_DIR

# External libraries
import frontmatter

class Episode:
    def __init__(self, file_name):
        self.__file_name = file_name
        with open(file_name) as f:
            self.__episode_frontmatter = frontmatter.load(f)

    def get(self, key):
        return self.__episode_frontmatter.get(key)

    def get_number(self, leading_zero=False):
        """
        Retrieves the episode number from the episode filename.
        A podcast episode filename is like `94-die-realität-des-freelancings-zwischen-selbstbestimmung-und-unsicherheit-mit-index-out-of-bounds.md`
        In the example, 94 is the episode number.

        Input: ../src/content/podcast/04-lohnt-der-einstieg-in-open-source.md
        Output (leading_zero=False): 4
        Output (leading_zero=True): 04

        Input: ../src/content/podcast/12-make-oder-buy.md
        Output: 12

        TODO Copied code from episode finder - How do we do it smarter?
        """
        filename = ntpath.basename(self.__file_name)
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

    def has_transcript(self, check_on_disk=False) -> bool:
        """
        Checks if the given {episode_number} (e.g. 94) has a transcript.
        Returns True is yes, False otherwise.
        """
        if len(self.get('transcript_slim')) > 0 and check_on_disk is False:
            return True

        if check_on_disk:
            episode_number = self.get_number(leading_zero=True)
            transcript_file = f"{episode_number}-transcript-slim.json"
            file_path = build_correct_file_path(TRANSCRIPT_STORAGE_DIR) + '/' + transcript_file
            print(file_path)
            exists = os.path.exists(file_path)
            if exists:
                self.__episode_frontmatter['transcript_slim'] = file_path
            return exists

        return False
