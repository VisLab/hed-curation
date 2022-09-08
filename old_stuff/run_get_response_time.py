import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import os


def find_task_files(bids_dir):
    file_end = '*_events.tsv'
    return [path for path in Path(bids_dir).rglob(file_end) if 'stopsignal' in str(path)]


if __name__ == '__main__':
    bids_dir = 'T:/ds002790-backup'
    # parser = argparse.ArgumentParser(description="""Count the number of go, successful stop and unsuccessful stop.""")
    # parser.add_argument('-d', dest='bids_dir', help='The root directory of the BIDS dataset.')
    # args = parser.parse_args()
    # events_path = find_task_files(args.bids_dir)

    events_path = find_task_files(bids_dir)
    total_events = 0
    total_times = 0.0
    for index, path in enumerate(events_path):
        events = pd.read_csv(path, sep='\t')
        xindex = ~events['response_time'].map(str).isin(['n/a'])
        total_times = total_times + events.loc[xindex, 'response_time'].sum()
        total_events = total_events + sum(xindex)
        break
    print(f"Total events {total_events} average response {total_times/total_events}")