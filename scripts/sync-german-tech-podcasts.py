import os
import logging
import tempfile 
import json
import shutil

from git import Repo
from PIL import Image

# Global variables
GIT_REPO = "https://github.com/EngineeringKiosk/GermanTechPodcasts.git"
GIT_REPO_NAME = "GermanTechPodcasts"
JSON_PATH_IN_GIT_REPO = "generated"
IMAGES_PATH_IN_GIT_REPO = "generated/images"
OPML_FILE_PATH_IN_GIT_REPO = "podcasts.opml"
PODCAST_JSON_FILE = 'src/data/german-tech-podcasts.json'
IMAGE_STORAGE = "public/images/german-tech-podcasts/"
OPML_STORAGE = "public/deutsche-tech-podcasts/podcasts.opml"


def sync_german_tech_podcasts(merged_json_file_path, image_storage_path, opml_storage_path):
    tmp_dir = tempfile.gettempdir()
    tmp_clone_dir = os.path.join(tmp_dir, GIT_REPO_NAME)
    
    # Cloning git repository
    logging.info(f"Cloning {GIT_REPO} into {tmp_clone_dir}...")
    Repo.clone_from(GIT_REPO, tmp_clone_dir)
    logging.info(f"Cloning {GIT_REPO} into {tmp_clone_dir}... successful")
    
    # Reading JSON files
    json_file_dir = os.path.join(tmp_clone_dir, JSON_PATH_IN_GIT_REPO)
    json_files = [json_file for json_file in os.listdir(json_file_dir) if json_file.endswith('.json')]
    logging.info(f"Found {len(json_files)} JSON files in {json_file_dir}")
    
    # Read and combine JSON Podcast data
    logging.info(f"Merging {len(json_files)} JSON files into one ...")
    podcast_data = []
    for json_file in json_files:
        abs_file_path = os.path.join(json_file_dir, json_file)
        with open(abs_file_path) as f:
            data = json.load(f)
            podcast_data.append(data)

    # Dump Podcast data into file
    logging.info(f"Writing merged JSON file {merged_json_file_path} ...")
    with open(merged_json_file_path, 'w') as fp:
        json.dump(podcast_data, fp, indent=4)

    # Copy images over
    # Right now we only do it oneway.
    # If a podcast updates its image, we don't delete the old one.
    # Dirty? Maybe. However, fast for now and the assumption is, that thos
    # will not happen very often. If this assumption is wrong, we will update the
    # piece of code below.
    images_file_dir = os.path.join(tmp_clone_dir, IMAGES_PATH_IN_GIT_REPO)
    image_files = [image_file for image_file in os.listdir(images_file_dir) if not image_file.startswith(".")]
    logging.info(f"Found {len(image_files)} image files in {images_file_dir}")

    for image_file in image_files:
        # Copy files over
        src = os.path.join(tmp_clone_dir, IMAGES_PATH_IN_GIT_REPO, image_file)
        dst = os.path.join(image_storage_path, image_file)
        logging.info(f"Copying {image_file} from {src} to {dst}...")
        shutil.copy2(src, dst)

        # Resize images
        image_to_resize = Image.open(dst)
        if image_to_resize.width > 700 and image_to_resize.height > 700:
            logging.info(f"Resizing {image_file} from {image_to_resize.width}x{image_to_resize.height} to 700x700...")
            resized_image = image_to_resize.resize((700, 700))
            resized_image.save(dst)

    # Copy OPML file over
    # Existing files will be replaced.
    src = os.path.join(tmp_clone_dir, OPML_FILE_PATH_IN_GIT_REPO)
    logging.info(f"Copying {src} to {opml_storage_path} ...")
    shutil.copy2(src, opml_storage_path)
    logging.info(f"Copying {src} to {opml_storage_path} ... done")

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
    image_storage_path = f"{folder_prefix}{IMAGE_STORAGE}"
    opml_storage_path = f"{folder_prefix}{OPML_STORAGE}"

    sync_german_tech_podcasts(merged_json_file_path, image_storage_path, opml_storage_path)