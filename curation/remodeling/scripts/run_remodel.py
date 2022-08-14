import os
import json
import argparse
from hed.util import get_file_list
from curation.remodeling.operations.dispatcher import Dispatcher


def main():
    parser = argparse.ArgumentParser(description="Converts event files based on a json file specifying operations.")
    parser.add_argument("data_dir", help="Full path of dataset root directory.")
    parser.add_argument("-m", "--model-path", dest="json_remodel_path", help="Full path of the remodel file.")
    parser.add_argument("-t", "--task-name", dest="task_name", help="The name of the task.")
    parser.add_argument("-e", "--extensions", nargs="*", default=[], dest="extensions",
                        help="Directories names to exclude from search for files.")
    parser.add_argument("-x", "--exclude-dirs", nargs="*", default=[], dest="exclude_dirs",
                        help="Directories names to exclude from search for files.")
    parser.add_argument("-s", "--file-suffix", dest="file_suffix", default='_events',
                        help="Filename suffix including file type.")
    parser.add_argument("-z", "--hed-schema", nargs="*", default=[], dest="hed_versions",
                        help="HED schema versions to load if HED is used.")
    args = parser.parse_args()

    command_path = os.path.realpath(args.json_remodel_path)
    with open(command_path, 'r') as fp:
        commands = json.load(fp)
    command_list, errors = Dispatcher.parse_commands(commands)
    if errors:
        raise ValueError("UnableToFullyParseCommands",
                         f"Fatal command errors, cannot continue:\n{Dispatcher.errors_to_str(errors)}")
    data_dir = os.path.realpath(args.data_dir)
    if not os.path.isdir(data_dir):
        raise ValueError("DataDirectoryDoesNotExist", f"The root data directory {data_dir} does not exist")
    dispatch = Dispatcher(commands, data_dir)
    event_files = get_file_list(data_dir, name_suffix=args.file_suffix, extensions=args.extensions)

    for events_file_path in event_files:
        the_path = os.path.realpath(events_file_path)
        print(the_path)
        events_df = dispatch.run_operations(the_path)
        # eventually save the events_df.
    for context_name, context_item in dispatch.context_dict.items():
        print(f"\n{context_item.get_text_summary(title=context_name)}")
    print("to_here")


if __name__ == '__main__':
    main()