# Scripts collection

## Install

```sh
$ make init
$ . venv/bin/activate
```

## Transcribe a podcast episode

Select a podcast episode which you want to transcribe.
Lets say episode 90.

```sh
$ ASSEMBLYAI_API_KEY="<API KEY>" python transcribe_published_episode.py 90
```

This will write the full raw data into `src/data/transcripts`.
We don't need the full raw data.
That's why we trim it a bit to a slim version and compress the original raw data for later usage:

```sh
$ python trim_transcribe_raw_data.py
```

The raw data contains a speaker detection with the label Speaker A, Speaker B, ...
We need to create a mapping who is Speaker A.
Go to your episode `.md` file (in this case `src/content/podcast/90-inner-source-open-source-best-practices-zur-besseren-zusammenarbeit-zwischen-teams-mit-sebastian-spier.md`) and edit

```toml
speaker:
- name: Andy Grunwald
- name: Wolfi Gassler
- name: Sebastian Spier
```

into

```toml
speaker:
- name: Andy Grunwald
  transcriptLetter: B
- name: Wolfi Gassler
  transcriptLetter: A
- name: Sebastian Spier
  transcriptLetter: C
```

You may want to check the Audio and the Transcript on who starts speaking.

Thats is everything.
Commit. Deploy. And enjoy the transcription on the website.

## Transcribe an audio file

```sh
ASSEMBLYAI_API_KEY="<API KEY>" python transcribe_audio_file.py --url https://my.file.com/foo.mp3 --speaker 3
```

## Script `podcast_feed_to_content.py`

A script that parses our Podcast XML Feed and generates the correct content files for our website.
