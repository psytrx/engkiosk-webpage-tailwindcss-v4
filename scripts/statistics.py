import os
from os.path import isfile, join
import json
import logging
import re

# External libraries
import frontmatter

# Global variables
PATH_EPISODE_MARKDOWN_FILES = 'src/pages/podcast/episode'
PATH_BLOG_MARKDOWN_FILES = 'src/pages/blog/post'
PATH_PODCAST_INFO_JSON_FILE = 'src/data/podcast-info.json'
PATH_TAGS_JSON_FILE = 'src/data/tags.json'

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)

def build_episode_statistics(path_md_files) -> dict:
    """
    Going through all Podcast Episode Markdown files and collect
    and calculate some basic statistics.
    """
    stats = dict()
    stats['number_of_episodes'] = 0
    stats['total_length_seconds'] = 0

    # Get existing podcast episodes
    episodes = [f for f in os.listdir(path_md_files) if isfile(join(path_md_files, f)) and f.endswith('.md')]
    for episode in episodes:
        file_path = f"{path_md_files}/{episode}"
        with open(file_path) as f:
            episode_frontmatter = frontmatter.load(f)
            
            stats['number_of_episodes'] += 1
            stats['total_length_seconds'] += episode_frontmatter['length_second']
            
    return stats


def build_tags_statistics(file_path) -> dict:
    """
    Collect and calculate some basic statistics about the
    tags used in the podcast.
    """

    stats = dict()
    stats['top_5_tags'] = 0
    stats['total_num_tags'] = 0

    with open(file_path) as f:
        data = json.load(f)

        # Sort tags
        # >= Python 3.7 dicts are sorted
        tags = dict(sorted(data.items(), key=lambda x: x[1]['usage_count'], reverse=True))
        stats['total_num_tags'] = len(tags)

        top_five = []
        for k, v in tags.items():
            s = f"{k} ({v['usage_count']} times)"
            top_five.append(s)

            if len(top_five) == 5:
                break

        stats['top_5_tags'] = top_five

    return stats


def build_blog_statistics(path_md_files) -> dict:
    """
    Going through all Blog Markdown files and collect
    and calculate some basic statistics.
    """
    stats = dict()
    stats['number_of_blog_posts'] = 0

    # Get existing podcast episodes
    posts = [f for f in os.listdir(path_md_files) if isfile(join(path_md_files, f)) and f.endswith('.mdx')]
    for post in posts:
        file_path = f"{path_md_files}/{post}"
        with open(file_path) as f:
            post_frontmatter = frontmatter.load(f)
            
            stats['number_of_blog_posts'] += 1
            # TODO Check what information is useful from the blog frontmatter
            
    return stats


def build_podcast_statistics(file_path) -> dict:
    """
    Collect and calculate some basic statistics about the
    basic podcast data.
    """
    stats = dict()

    with open(file_path) as f:
        data = json.load(f)

        stats["number_of_plattforms"] = len(data["platformLinks"])
        stats["plattforms"] = sentence_case(", ".join(data["platformLinks"].keys()))
    
    return stats


def sentence_case(string):
    if string != '':
        result = re.sub('([A-Z])', r' \1', string)
        return result[:1].upper() + result[1:].lower()
    return


def get_time_human_readable(seconds, granularity=4) -> str:
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))

    return ', '.join(result[:granularity])


def get_correct_path(p) -> str:
    # Determine if the script is called from root
    # or from the scripts directory.
    directory_path = os.getcwd()
    folder_name = os.path.basename(directory_path)
    if folder_name == "scripts":
        p = f"../{p}"

    return p


def print_stats(stats):
    seconds_per_episode_avg = stats['total_length_seconds'] / stats['number_of_episodes']

    print("Engineering Kiosk Summary")
    print("=========================")
    print("Podcast")
    print('-----------------')
    print(f"Available on platforms: {stats['number_of_plattforms']}")
    print(f"Platforms: {stats['plattforms']}")
    print("")
    print("Podcast Episodes")
    print('-----------------')
    print(f"Number of episodes: {stats['number_of_episodes']}")
    print(f"Total length of content: {get_time_human_readable(stats['total_length_seconds'])}")
    print(f"Avg of episode length: {get_time_human_readable(seconds_per_episode_avg)}")
    print(f"Number of tags: {stats['total_num_tags']}")
    print(f"Top 5 tags:")
    for v in stats['top_5_tags']:
         print(f"\t{v}")
    print("")
    print("Blog posts")
    print('-----------------')
    print(f"Number of blog posts: {stats['number_of_blog_posts']}")


if __name__ == "__main__":
    # Setup logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    stats = dict()

    # Collecting data
    episode_stats = build_episode_statistics(get_correct_path(PATH_EPISODE_MARKDOWN_FILES))
    blog_stats = build_blog_statistics(get_correct_path(PATH_BLOG_MARKDOWN_FILES))
    tags_stats = build_tags_statistics(get_correct_path(PATH_TAGS_JSON_FILE))
    podcast_stats = build_podcast_statistics(get_correct_path(PATH_PODCAST_INFO_JSON_FILE))
    
    # Merging dicts
    stats = stats | episode_stats
    stats = stats | tags_stats
    stats = stats | blog_stats
    stats = stats | podcast_stats

    print_stats(stats)