from curation.remodeling.operations.base_op import BaseOp

RENAME_PARAMS = {
    "command": "rename_columns",
    "required_parameters": {
        "column_mapping": dict,
        "ignore_missing": bool
    },
    "optional_parameters": {}
}


class RenameColumnsOp (BaseOp):
    """ Rename columns in a dataframe.

    Notes: The required parameters are:
        - column_mapping (dict) The names of the columns to be removed.
        - ignore_missing (bool) If true, the names in remove_names that are not columns in df should be ignored.

    Raises:
        KeyError if ignore_missing is false and a column name in column_mapping is not in the dataframe.

    """

    def __init__(self, parameters):
        super().__init__(RENAME_PARAMS["command"], RENAME_PARAMS["required_parameters"],
                         RENAME_PARAMS["optional_parameters"])
        self.check_parameters(parameters)
        self.column_mapping = parameters['column_mapping']
        if parameters['ignore_missing']:
            self.error_handling = 'ignore'
        else:
            self.error_handling = 'raise'

    def do_op(self, df):
        """ Rename columns as specified in column_mapping dictionary.

        Args:
            df (DataFrame) - The DataFrame whose columns are to be renamed.

        Returns:
            DataFrame - a new dataframe with columns renamed.


        Raises:
            KeyError - when ignore_missing is false and column_mapping has columns not in df.

        """

        return df.rename(columns=self.column_mapping, errors=self.error_handling)
