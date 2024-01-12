import logging
import sys
import os
from os.path import isfile, join
import zipfile
import json

from functions import TRANSCRIPT_STORAGE_DIR, build_correct_file_path


if __name__ == "__main__":
    # Setup logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    logging.info("Searching for raw and uncompressed transcription data ...")

    storage_dir = build_correct_file_path(TRANSCRIPT_STORAGE_DIR)
    uncompressed_suffix = "-transcript.json"
    raw_transcriptions = [f for f in os.listdir(storage_dir) if isfile(join(storage_dir, f)) and f.endswith(uncompressed_suffix)]

    logging.info(f"Searching for raw and uncompressed transcription data ... {len(raw_transcriptions)} found")
    if len(raw_transcriptions) == 0:
        logging.info("Nothing to do here")
        sys.exit(0)

    for transcription_file in raw_transcriptions:
        full_transcript_filepath = f"{storage_dir}/{transcription_file}"

        logging.info(f"Processing {full_transcript_filepath} ...")

        with open(full_transcript_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Make data more slim and delete things we don't need
            del data["text"]
            del data["words"]
            del data["iab_categories_result"]

            for i, utterance in enumerate(data["utterances"]):
                del data["utterances"][i]["words"]

            # Write slim version to disk
            slim_filename = transcription_file.removesuffix('.json')
            slim_filename = f"{slim_filename}-slim.json"

            slim_transcript_filepath = f"{storage_dir}/{slim_filename}"
            logging.info(f"Writing slim transcription data to disk to {slim_transcript_filepath} ...")
            with open(slim_transcript_filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            logging.info(f"Writing slim transcription data to disk to {slim_transcript_filepath} ... Success")

        # Compressing raw data
        raw_zip_filename = transcription_file.removesuffix('.json')
        zip_archive_name = f"{storage_dir}/{raw_zip_filename}.zip"
        logging.info(f"Compressing {full_transcript_filepath} into {zip_archive_name} ...")
        zipfile.ZipFile(zip_archive_name, mode='w', compression=zipfile.ZIP_DEFLATED).write(full_transcript_filepath, arcname=transcription_file)
        logging.info(f"Compressing {full_transcript_filepath} into {zip_archive_name} ... Success")

        # Deleting raw data file
        # We don't need it anymore, because we compressed it
        logging.info(f"Deleting {full_transcript_filepath} ...")
        os.remove(full_transcript_filepath)
        logging.info(f"Deleting {full_transcript_filepath} ... Success")
