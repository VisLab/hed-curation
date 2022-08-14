import numpy as np
from curation.remodeling.util.base import tuple_to_range, get_indices
from curation.remodeling.operations.base_op import BaseOp

PARAMS = {
    "command": "add_structure_numbers",
    "required_parameters": {
        "column_name": str,
        "remove_values": list
    },
    "optional_parameters": {}
}


class AddStructureNumbersOp(BaseOp):

    def __init__(self, parameters):
        super().__init__(PARAMS["command"], PARAMS["required_parameters"], PARAMS["optional_parameters"])
        self.check_parameters(parameters)
        self.trial_dict = {}

    def do_op(self, dispatcher, df, name, sidecar=None):
        # TODO: this is not written
        """ Add structure numbers.

        Args:
            dispatcher (Dispatcher) - dispatcher object for context
            df (DataFrame) - The DataFrame to be remodeled.
            name (str) - Unique identifier for the dataframe -- often the original file path.
            sidecar (Sidecar or file-like)   Only needed for HED operations

        Returns:
            Dataframe - a new dataframe after processing.

        """

        df['trial'] = np.nan
        block_indices = tuple_to_range(get_indices(df, self.trial_dict['block']['marker_column'],
                                                   self.trial_dict['block']['marker_list']))
        trial_indices = tuple_to_range(get_indices(df, self.trial_dict['trial']['marker_column'],
                                                   self.trial_dict['trial']['marker_list']))

        block_separated = []
        for block_sublist in block_indices:
            new_block_list = []
            for trial_sublist in trial_indices:
                if trial_sublist[0] in block_sublist:
                    new_block_list.append(trial_sublist)
            block_separated.append(new_block_list)

        for block in block_separated:
            count = 0
            for trial in block:
                count += 1
                df.loc[trial, 'trial'] = count
        return df
