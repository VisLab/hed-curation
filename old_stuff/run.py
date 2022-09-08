import argparse
import pandas as pd
from operations.ops import run_operations

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""Converts event files based on a json file specifying
        operations.""")
    parser.add_argument(
        "-d",
        dest="bids_dir",
        help="")
    parser.add_argument(
        "-t",
        dest="task_name",
        help="")
    parser.add_argument(
        "-o",
        dest="operations_json_path",
        help="")
    args = parser.parse_args()

    all_events_paths = bids.find_task_files(args.bids_dir, args.task_name)
    operations_dict = bids.load_operations(args.operations_json_path)

    for events_file_path in all_events_paths:
        print('Loading file: %s' % events_file_path)
        print('')
        events = pd.read_csv(events_file_path, sep='\t', index=False)

        print('Restructuring %s' % events_file_path)
        events = run_operations(events, operations_dict)
        bids.rename_and_save_new(events, events_file_path)
