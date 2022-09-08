import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import os

parser = argparse.ArgumentParser(
    description='''Get behavioural data stop signal task.''')

parser.add_argument(
    '-d',
    dest='bids_dir',
    help='')

parser.add_argument(
    '--adapted',
    dest='adapted',
    action='store_true',
    help=''
)

args = parser.parse_args()


def find_task_files(bids_dir, adapted):
    file_end = '*_events_orig.tsv' if adapted else '*_events.tsv'
    return [path for path in Path(bids_dir).rglob(file_end) if
            'stopsignal' in str(path)]


all_events_path = find_task_files(args.bids_dir, args.adapted)

all_data = pd.DataFrame([], columns=['sub', 'trial_number', 'sex',
                                     'response_hand', 'response_accuracy',
                                     'reaction_time'])

for path in all_events_path:
    events = pd.read_csv(path, sep='\t')
    sub = os.path.normpath(path).split(os.sep)[1]
    all_data = pd.concat([all_data, pd.DataFrame({
        'sub': sub,
        'trial_number': np.array(events.index) + 1,
        'reaction_time': events['response_time'],
        'sex': events['sex'],
        'response_hand': events['response_hand'],
        'response_accuracy': events['response_accuracy']
        })])

out = os.path.join(args.bids_dir, 'derivatives/beh/reaction_times.tsv')
os.makedirs(os.path.dirname(out), exist_ok=True)
all_data.to_csv(out, sep='\t')
