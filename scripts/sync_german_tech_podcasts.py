import os
import json
import logging
import tempfile
import shutil

from functions import (
    build_correct_file_path
)

from constants import (
    GERMAN_TECH_PODCAST_GIT_REPO,
    GERMAN_TECH_PODCAST_GIT_REPO_NAME,
    GERMAN_TECH_PODCAST_JSON_PATH_IN_GIT_REPO,
    GERMAN_TECH_PODCAST_IMAGES_PATH_IN_GIT_REPO,
    GERMAN_TECH_PODCAST_OPML_FILE_PATH_IN_GIT_REPO,
    GERMAN_TECH_PODCAST_JSON_STORAGE,
    GERMAN_TECH_PODCAST_IMAGE_STORAGE,
    GERMAN_TECH_PODCAST_OPML_STORAGE
)

from git import Repo
from PIL import Image

def sync_german_tech_podcasts(json_storage_path, image_storage_path, opml_storage_path):
    tmp_dir = tempfile.gettempdir()
    tmp_clone_dir = os.path.join(tmp_dir, GERMAN_TECH_PODCAST_GIT_REPO_NAME)
    
    # Cloning git repository
    logging.info(f"Cloning {GERMAN_TECH_PODCAST_GIT_REPO} into {tmp_clone_dir}...")
    Repo.clone_from(GERMAN_TECH_PODCAST_GIT_REPO, tmp_clone_dir)
    logging.info(f"Cloning {GERMAN_TECH_PODCAST_GIT_REPO} into {tmp_clone_dir}... successful")
    
    # Reading JSON files
    json_file_dir = os.path.join(tmp_clone_dir, GERMAN_TECH_PODCAST_JSON_PATH_IN_GIT_REPO)
    json_files = [json_file for json_file in os.listdir(json_file_dir) if json_file.endswith('.json')]
    logging.info(f"Found {len(json_files)} JSON files in {json_file_dir}")
    
    # Copy JSON files over
    for json_file in json_files:
        # Copy files over
        src = os.path.join(tmp_clone_dir, GERMAN_TECH_PODCAST_JSON_PATH_IN_GIT_REPO, json_file)
        dst = os.path.join(json_storage_path, json_file)
        logging.info(f"Copying {json_file} from {src} to {dst}...")
        shutil.copy2(src, dst)

        # Modify file content
        with open(dst) as f:
            data = json.load(f)
            # Modify image key to only contain the filename
            data["image"] = f"./{os.path.basename(data['image'])}"

        # Write new file content
        with open(dst, 'w') as fp:
            json.dump(data, fp, indent=4)

    # Copy images over
    # Right now we only do it oneway.
    # If a podcast updates its image, we don't delete the old one.
    # Dirty? Maybe. However, fast for now and the assumption is, that this
    # will not happen very often. If this assumption is wrong, we will update the
    # piece of code below.
    images_file_dir = os.path.join(tmp_clone_dir, GERMAN_TECH_PODCAST_IMAGES_PATH_IN_GIT_REPO)
    image_files = [image_file for image_file in os.listdir(images_file_dir) if not image_file.startswith(".")]
    logging.info(f"Found {len(image_files)} image files in {images_file_dir}")

    for image_file in image_files:
        # Copy files over
        src = os.path.join(tmp_clone_dir, GERMAN_TECH_PODCAST_IMAGES_PATH_IN_GIT_REPO, image_file)
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
    src = os.path.join(tmp_clone_dir, GERMAN_TECH_PODCAST_OPML_FILE_PATH_IN_GIT_REPO)
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

    image_storage_path = build_correct_file_path(GERMAN_TECH_PODCAST_IMAGE_STORAGE)
    json_storage_path = build_correct_file_path(GERMAN_TECH_PODCAST_JSON_STORAGE)
    opml_storage_path = build_correct_file_path(GERMAN_TECH_PODCAST_OPML_STORAGE)

    sync_german_tech_podcasts(json_storage_path, image_storage_path, opml_storage_path)