import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import os


def find_task_files(bids_dir):
    file_end = '*_events.tsv'
    return [path for path in Path(bids_dir).rglob(file_end) if 'stopsignal' in str(path)]


if __name__ == '__main__':
    bids_dir = 'T:/ds002790-test'
    # parser = argparse.ArgumentParser(description="""Count the number of go, successful stop and unsuccessful stop.""")
    # parser.add_argument('-d', dest='bids_dir', help='The root directory of the BIDS dataset.')
    # args = parser.parse_args()
    # events_path = find_task_files(args.bids_dir)

    events_path = find_task_files(bids_dir)
    counts = pd.DataFrame(np.zeros(shape=[len(events_path), 3]), columns=['go', 'succesful_stop', 'unsuccesful_stop'])
    for index, path in enumerate(events_path):
        events = pd.read_csv(path, sep='\t')
        x = sum(events['trial_type'].map(str).isin(['go']))
        counts.loc[index, 'go'] = sum(events['trial_type'].map(str).isin(['go']))
        counts.loc[index, 'succesful_stop'] = sum(events['trial_type'].map(str).isin(['succesful_stop']))
        counts.loc[index, 'unsuccesful_stop'] = sum(events['trial_type'].map(str).isin(['unsuccesful_stop']))

    out = os.path.join(bids_dir, 'derivatives/beh/trial_counts.tsv')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    counts.to_csv(out, sep='\t', index=False)
