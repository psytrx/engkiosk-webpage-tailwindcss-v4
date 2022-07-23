import os
import logging
import tempfile 
import json
import shutil

from git import Repo


# Global variables
GIT_REPO = "https://github.com/EngineeringKiosk/GermanTechPodcasts.git"
GIT_REPO_NAME = "GermanTechPodcasts"
JSON_PATH_IN_GET_REPO = "generated"
PODCAST_JSON_FILE = 'src/data/german_tech_podcasts.json'


def sync_german_tech_podcasts(merged_json_file_path):
    tmp_dir = tempfile.gettempdir()
    tmp_clone_dir = os.path.join(tmp_dir, GIT_REPO_NAME)
    
    # Cloning git repository
    logging.info(f"Cloning {GIT_REPO} into {tmp_clone_dir}...")
    Repo.clone_from(GIT_REPO, tmp_clone_dir)
    logging.info(f"Cloning {GIT_REPO} into {tmp_clone_dir}... successful")
    
    # Reading JSON files
    json_file_dir = os.path.join(tmp_clone_dir, JSON_PATH_IN_GET_REPO)
    json_files = [json_file for json_file in os.listdir(json_file_dir) if json_file.endswith('.json')]
    logging.info(f"Found {len(json_files)} JSON files in {json_file_dir}")
    
    # Read and combine Podcast data
    logging.info(f"Merging {len(json_files)} JSON files into one ...")
    podcast_data = {}
    for json_file in json_files:
        abs_file_path = os.path.join(json_file_dir, json_file)
        with open(abs_file_path) as f:
            data = json.load(f)
            podcast_data[data["name"]] = data

    logging.info(f"Writing merged JSON file {merged_json_file_path} ...")
    # Dump Podcast data into file
    with open(merged_json_file_path, 'w') as fp:
        json.dump(podcast_data, fp, indent=4)

    # Removing git clone
    logging.info(f"Removing cloned repository from merged JSON file {tmp_clone_dir}...")
    shutil.rmtree(tmp_clone_dir)

    logging.info("Aaaaand we are done")


if __name__ == "__main__":
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

    merged_json_file_path = f"{folder_prefix}{PODCAST_JSON_FILE}"

    sync_german_tech_podcasts(merged_json_file_path)