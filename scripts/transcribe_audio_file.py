import argparse
import logging
import sys
import os
import assemblyai as aai
import json
import validators


if __name__ == "__main__":
    cli_parser = argparse.ArgumentParser(
        description='Transcribe an audio file')

    cli_parser.add_argument('-u', '--url', type=str,
                            required=True, help='Audio file URL to transcribe')
    cli_parser.add_argument('-s', '--speaker', type=int, const=2,
                            nargs='?', help='Number of speaker in the audio file')
    cli_parser.add_argument('-o', '--output', type=str,
                            default=None, nargs='?', help='Output filename')
    args = cli_parser.parse_args()

    # Setup logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    # URL validation
    if not validators.url(args.url):
        logging.error("Please enter a valud url")
        sys.exit(1)

    # if no output filename is given, use the filename from the url
    if not args.output:
        args.output = args.url.split('/')[-1].split('.')[0] + '.json'

    logging.info(f"Audio url: {args.url}")
    logging.info(f"Number of speaker: {args.speaker}")
    logging.info(f"Output file: {args.output}")

    ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')
    if not ASSEMBLYAI_API_KEY:
        logging.error("No ASSEMBLYAI_API_KEY available")
        sys.exit(1)

    # Generate transcript
    aai.settings.api_key = ASSEMBLYAI_API_KEY
    logging.info("Assemblyai API Key found")

    logging.info("Requesting transcript ...")
    transcriber = aai.Transcriber()
    audio_url = (
        args.url
    )
    # https://www.assemblyai.com/docs/api-reference/transcript
    config = aai.TranscriptionConfig(
        speaker_labels=True,
        speakers_expected=args.speaker,
        language_code="de",
        punctuate=True,
        content_safety=False,
        # disfluencies=True,  # if true, transcribe "uhm" and "ahm" but only in english
        # Not supported with our language
        # auto_highlights=True,
        # summarization=True,
        # summary_model=aai.SummarizationModel.conversational,
        # summary_type=aai.SummarizationType.paragraph,
        # entity_detection=True,
    )
    transcript = transcriber.transcribe(audio_url, config)
    logging.info("Requesting transcript ... Success")

    logging.info(f"Writing transcript to disk to {args.output} ...")
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(transcript.json_response, f, ensure_ascii=False, indent=4)

    logging.info(f"Writing transcript to disk to {args.output} ... Success")
