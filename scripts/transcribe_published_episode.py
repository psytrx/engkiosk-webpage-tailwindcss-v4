import argparse
import logging
import sys
import os
import assemblyai as aai
import json

from episode_finder import (
    EpisodeFinder
)

from functions import EPISODES_STORAGE_DIR, TRANSCRIPT_STORAGE_DIR, build_correct_file_path


if __name__ == "__main__":
    cli_parser = argparse.ArgumentParser(description='Transcribe a podcast episode')
    cli_parser.add_argument('Episode',
        metavar='episode',
        type=int,
        help='Episode to process for transcription. Example value: "68"')
    args = cli_parser.parse_args()

    # Setup logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    # We have one -1 and one 00 Episode.
    # Disallow other older ones.
    if args.Episode <= -2:
        logging.error("Please enter an episode number. E.g. 43")
        sys.exit(1)

    # Sometimes we get "3", but we need "03"
    episode_number = str(args.Episode)
    episode_number = episode_number.zfill(2)

    logging.info(f"Searching for podcast episode {episode_number} ...")
    p = build_correct_file_path(EPISODES_STORAGE_DIR)
    episode_finder = EpisodeFinder(p)
    episode = episode_finder.get_podcast_episode_by_number(episode_number)
    if episode is None:
        logging.info(f"Searching for podcast episode {episode_number} ... Not found")
        sys.exit(1)

    logging.info(f"Searching for podcast episode {episode_number} ... Found")

    episode_audio_url = episode.get("audio")
    if not episode_audio_url:
        logging.error("No audio url available")
        sys.exit(1)
    logging.info(f"Podcast episode audio url: {episode_audio_url}")

    episode_speaker_num = len(episode.get("speaker"))
    logging.info(f"Podcast episode speaker: {episode_speaker_num}")

    ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')
    if not ASSEMBLYAI_API_KEY:
        logging.error("No ASSEMBLYAI_API_KEY available")
        sys.exit(1)

    # Generate transcript
    aai.settings.api_key = ASSEMBLYAI_API_KEY
    logging.info("Assemblyai API Key found")

    logging.info("Requesting podcast episode transcript ...")
    transcriber = aai.Transcriber()
    audio_url = (
        episode_audio_url
    )
    # https://www.assemblyai.com/docs/api-reference/transcript
    config = aai.TranscriptionConfig(
        speaker_labels=True,
        speakers_expected=episode_speaker_num,
        language_code="de", 
        punctuate=True, 
        content_safety=False, 
        # Not supported with our language
        # auto_highlights=True,
        #summarization=True,
        #summary_model=aai.SummarizationModel.conversational,
        #summary_type=aai.SummarizationType.paragraph,
        #entity_detection=True,
    )
    transcript = transcriber.transcribe(audio_url, config)
    logging.info("Requesting podcast episode transcript ... Success")
    
    transcript_filename = f"{episode_number}-transcript.json"
    full_transcript_filepath = f"{build_correct_file_path(TRANSCRIPT_STORAGE_DIR)}/{transcript_filename}"

    logging.info(f"Writing podcast episode transcript to disk to {full_transcript_filepath} ...")
    with open(full_transcript_filepath, 'w', encoding='utf-8') as f:
        json.dump(transcript.json_response, f, ensure_ascii=False, indent=4)
    
    logging.info(f"Writing podcast episode transcript to disk to {full_transcript_filepath} ... Success")
