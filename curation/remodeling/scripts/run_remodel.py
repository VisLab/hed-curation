import os
import json
import argparse
from hed.schema import load_schema_version
from hed.util import get_file_list
from hed.tools import BidsDataset
from curation.remodeling.operations.dispatcher import Dispatcher


def get_parser():
    parser = argparse.ArgumentParser(description="Converts event files based on a json file specifying operations.")
    parser.add_argument("data_dir", help="Full path of dataset root directory.")
    parser.add_argument("-m", "--model-path", dest="json_remodel_path", help="Full path of the remodel file.")
    parser.add_argument("-t", "--task-name", dest="task_name", help="The name of the task.")
    parser.add_argument("-e", "--extensions", nargs="*", default=['.tsv'], dest="extensions",
                        help="File extensions to allow in locating files.")
    parser.add_argument("-x", "--exclude-dirs", nargs="*", default=[], dest="exclude_dirs",
                        help="Directories names to exclude from search for files.")
    parser.add_argument("-f", "--file-suffix", dest="file_suffix", default='events',
                        help="Filename suffix including file type.")
    parser.add_argument("-b", "--bids-format", dest="use_bids",
                        help="If present, the dataset is in BIDS format with sidecars.")
    parser.add_argument("-v", "--verbose", action='store_true',
                        help="If present, output informative messages as computation progresses.")
    return parser


def run_bids_ops(dispatch, args):
    verbose = hasattr(args, 'verbose')
    bids = BidsDataset(dispatch.data_root, tabular_types=['events'], exclude_dirs=args.exclude_dirs)
    dispatch.hed_schema = bids.schema
    if verbose:
        print(f"Successfully parsed BIDS dataset with HED schema {str(bids.get_schema_versions())}")
    events = bids.get_tabular_group(args.file_suffix)
    if verbose:
        print(f"Processing ")
    for events_obj in events.datafile_dict.values():
        sidecar_list = events.get_sidecars_from_path(events_obj)
        if sidecar_list:
            sidecar = events.sidecar_dict[sidecar_list[-1]].contents
        else:
            sidecar = None
        df = dispatch.run_operations(events_obj.file_path, sidecar=sidecar, verbose=verbose)
        # Eventually decide what to do with the files
    return


def run_direct_ops(dispatch, args):
    verbose = hasattr(args, 'verbose')
    tabular_files = get_file_list(dispatch.data_root, name_suffix=args.file_suffix, extensions=args.extensions,
                                  exclude_dirs=args.exclude_dirs)
    if verbose:
        print(f"Found {len(tabular_files)} files with suffix {args.file_suffix} and extensions {str(args.extensions)}")
    for file_path in tabular_files:
        df = dispatch.run_operations(file_path, verbose=True)
        # eventually save the events_df.


def main():
    parser = get_parser()
    args = parser.parse_args()
    verbose = hasattr(args, 'verbose')
    command_path = os.path.realpath(args.json_remodel_path)
    if verbose:
        print(f"Data directory: {args.data_dir}\nCommand path: {command_path}")
    with open(command_path, 'r') as fp:
        commands = json.load(fp)
    command_list, errors = Dispatcher.parse_commands(commands)
    if errors:
        raise ValueError("UnableToFullyParseCommands",
                         f"Fatal command errors, cannot continue:\n{Dispatcher.errors_to_str(errors)}")
    data_dir = os.path.realpath(args.data_dir)
    if not os.path.isdir(data_dir):
        raise ValueError("DataDirectoryDoesNotExist", f"The root data directory {data_dir} does not exist")
    dispatch = Dispatcher(commands, data_root=data_dir)
    if hasattr(args, "bids_format"):
        run_bids_ops(dispatch, args)
    else:
        run_direct_ops(dispatch, args)

    for context_name, context_item in dispatch.context_dict.items():
        print(f"\n{context_item.get_text_summary(title=context_name)}")
    print("to_here")


if __name__ == '__main__':
    main()
