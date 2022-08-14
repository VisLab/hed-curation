from curation.remodeling.operations.base_op import BaseOp

PARAMS = {
    "command": "add_structure_column",
    "required_parameters": {
        "column_name": str,
        "structure_dict": dict,
        "remove_values": list
    },
    "optional_parameters": {}
}


class AddStructureColumnOp(BaseOp):

    def __init__(self, parameters):
        super().__init__(PARAMS["command"], PARAMS["required_parameters"], PARAMS["optional_parameters"])
        self.check_parameters(parameters)
        self.structure_dict = {}

    def do_op(self, dispatcher, df, name, sidecar=None):
        """ Add column containing structure information.

        Args:
            dispatcher (Dispatcher) - dispatcher object for context
            df (DataFrame) - The DataFrame to be remodeled.
            name (str) - Unique identifier for the dataframe -- often the original file path.
            sidecar (Sidecar or file-like)   Only needed for HED operations

        Returns:
            Dataframe - a new dataframe after processing.

        """

        # dispatch = {'structure_column': structure.add_column_value,
        #             'structure_event': structure.add_summed_events}
        #
        # for element in self.structure_dict:
        #     process = self.structure_dict[element]
        #     indices = base.tuple_to_range(base.get_indices(df, process['marker_column'], process['marker_list']))
        #     column = (process['new_column'] if 'new_column' in process else process['marker_column'])
        #     value = (process['label'] if 'label' in process else element)
        #     number = process['number']
        #     df = dispatch[process.pop('type')](df, indices, column, value, number)
        return df.copy()
