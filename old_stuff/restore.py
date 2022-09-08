import argparse

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
    args = parser.parse_args()

    all_events_path = bids.find_task_files(args.bids_dir, args.task_name)

    for path in all_events_path:
        bids.remove_new_rename_old(path)
