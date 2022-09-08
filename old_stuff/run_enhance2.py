import argparse
import pandas as pd
# import curation.remapping.operations.ops as ops
from curation.remodeling.util.bidsfiles import find_task_files, load_operations, rename_and_save_new
# import .operations.bidsfiles
from curation.remodeling.operations.dispatcher import run_operations

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Converts event files based on a json file specifying operations.")
    parser.add_argument("-d", dest="bids_dir", help="Full path of BIDS root directory")
    parser.add_argument("-t", dest="task_name", help="The name of the task to make this enhancement.")
    parser.add_argument("-o", dest="remodeling_path", help="Path of the remodeling specification.")
    args = parser.parse_args()

    all_events_paths = find_task_files(args.bids_dir, args.task_name)
    operations_dict = load_operations(args.operations_json_path)

    for events_file_path in all_events_paths:
        print('Loading file: %s' % events_file_path)
        print('')
        events = pd.read_csv(events_file_path, sep='\t')

        print('Restructuring %s' % events_file_path)
        events = run_operations(events, operations_dict)
        rename_and_save_new(events, events_file_path)
