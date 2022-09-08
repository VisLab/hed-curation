import os
import argparse
from pathlib import Path
import json
import pandas as pd
import enhance_event




def find_task_files(bids_dir, task):
    return [path for path in Path(bids_dir).rglob('*_events.tsv') if task in str(path)]


# def load_operations(json_path):
#     with open(json_path, encoding='utf-8') as f:
#         operations_dict = json.load(f)
#     return operations_dict


def rename_and_save_new(df, path):
    os.rename(path, str(path)[:-4] + 'orig' + str(path)[-4:])
    df.to_csv(path, sep='\t', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Converts event files based on a json file specifying operations.""")
    parser.add_argument("-d", dest="bids_dir", help="")
    parser.add_argument("-t", dest="task_name", help="The name of the task to make this enhancement.")
    #parser.add_argument("-o", dest="operations_json_path", help="")
    args = parser.parse_args()
    print(f"Args: {str(args)}")
    all_events_paths = find_task_files(args.bids_dir, args.task_name)
    # operations_dict = load_operations(args.operations_json_path)

    for events_file_path in all_events_paths:
        print('Loading file: %s' % events_file_path)
        print('')
        events = pd.read_csv(events_file_path, sep='\t', header=0, keep_default_na=False, na_values=",null")

        print('Restructuring %s' % events_file_path)
        events["go_left"] = 0
        events["go_right"] = 0
        go_mask = events['trial_type'].map(str).isin(['go'])
        go_left = go_mask & events['response_hand'].map(str).isin(['left'])
        go_right = go_mask & events['response_hand'].map(str).isin(['right'])
        events.loc[go_left, "go_left"] = 1
        events.loc[go_right, "go_right"] = 1

        #events = enhance_event.enhance_events(events, operations_dict)
        rename_and_save_new(events, events_file_path)
