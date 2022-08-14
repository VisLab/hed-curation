import argparse
from curation.remodeling.util.bidsfiles import find_task_files, backup_events


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Converts event files based on a json file specifying operations.""")
    parser.add_argument("bids_dir", help="Dataset whose _orig_events.tsv become _events.tsv")
    parser.add_argument("output_dir", help="Help us")
    args = parser.parse_args()

    all_events_path = find_task_files(args.bids_dir)
    for event_path in all_events_path:
        backup_events(event_path)

