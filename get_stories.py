from fanfiction.scraper import Scraper
import pickle
import urllib.request
import argparse
import os
import pdb
import csv
from tqdm import tqdm
import timeit


def load_story_ids(fpath):
    """
    Returns list of story ids loaded from text file.
    """

    with open(fpath) as f:
        story_ids = [int(i) for i in f.read().splitlines()]

    return story_ids

def save_stories(scraper, ids, out_dirpath):

    metadata_out_fpath = os.path.join(out_dirpath, 'metadata.csv')
    columns = ["id", "canon_type", 'canon', 'author_id', 'title', 'updated', 'published', 'lang', 'genres', 'num_reviews', 'num_favs', 'num_follows', 'num_words', 'rated']
    with open(metadata_out_fpath, 'w') as f:
        w = csv.writer(f)
        w.writerow(columns)

    story_out_dirpath = os.path.join(out_dirpath, 'stories')
    if not os.path.exists(story_out_dirpath):
        os.mkdir(story_out_dirpath)

    for i in tqdm(ids):

        #try:
        #    story_metadata = scraper.scrape_story(i)

        #except:
        #    tqdm.write(f"No story found for ID {i}")
        #    continue

        story_metadata = scraper.scrape_story(i)

        # Save metadata
        with open(metadata_out_fpath, 'a') as f:
            w = csv.writer(f)
            w.writerow([story_metadata.get(col, '') for col in columns])

        # Save story
        story_out_fpath = os.path.join(story_out_dirpath, "{}.txt".format(story_metadata['id']))
        with open(story_out_fpath, 'w') as f:
            for c, story in story_metadata['chapters'].items():
                f.write(str(story) + '\n\n')


def main():
    parser = argparse.ArgumentParser(description="Scrape stories from a list of IDs.")
    parser.add_argument('ids_fpath', nargs='?', help="Filepath of file with list of IDs.")
    parser.add_argument('--out-directory', nargs='?', dest='out_dirpath', help="Path to directory where will save metadata CSV and story text files. Will be created if doesn't exist.")
    args = parser.parse_args()

    ids = load_story_ids(args.ids_fpath)

    if not os.path.exists(args.out_dirpath):
        os.makedirs(args.out_dirpath)

    scraper = Scraper(rate_limit=0.1)

    save_stories(scraper, ids, args.out_dirpath)

if __name__ == '__main__':
    main()
