import os
from os.path import isfile, join

# External libraries
import frontmatter

EPISODES_STORAGE_DIR = 'src/pages/podcast/episode'
TRANSCRIPT_STORAGE_DIR = 'src/data/transcripts'

def build_correct_file_path(file_path) -> str:
    """
    Build the correct path to files.

    If a python script gets called from `scripts` folder, 
    we need to get a level up.
    This function takes care about the correct path.
    """
    p = file_path

    # Determine if the script is called from root
    # or from the scripts directory.
    directory_path = os.getcwd()
    folder_name = os.path.basename(directory_path)
    if folder_name == "scripts":
        p = f"../{file_path}"
    
    return p


def get_podcast_episode_by_number(storage_dir, number):
    """
    Gets the podcast episode data by number.

    {storage_dir} is the storage where the podcast episodes are stored.
    {number} is the number of the podcast.

    If more than 1 or 0 podcast episodes are found, an exception is thrown.
    If the episode was found, the episode object is returned.
    """
    episode_prefix = f"{number}-"
    episode_suffix = '.md'

    # Get existing podcast episodes
    episodes = [f for f in os.listdir(storage_dir) if isfile(join(storage_dir, f)) and f.startswith(episode_prefix) and f.endswith(episode_suffix)]
    
    if len(episodes) > 1:
        raise Exception("More than one podcast episode found.")
    
    if len(episodes) == 0:
        raise Exception("No podcast episode found.")

    episode_filename = episodes[0]

    episode = None
    file_path = f"{storage_dir}/{episode_filename}"
    with open(file_path) as f:
        episode = frontmatter.load(f)

    return episode