from curation.remodeling.operations.base_op import BaseOp

PARAMS = {
    "command": "remove_columns",
    "required_parameters": {
        "remove_names": list,
        "ignore_missing": bool
    },
    "optional_parameters": {}
}


class RemoveColumnsOp(BaseOp):
    """ Remove columns from a dataframe.

    Notes: The required parameters are:
        - remove_names (list)      The names of the columns to be removed.
        - ignore_missing (boolean) If true, the names in remove_names that are not columns in df should be ignored.

    """

    def __init__(self, parameters):
        """ Constructor for remove columns command.

        Args:
            parameters (dict): A dictionary of the parameters for this command.

        Raises:
            KeyError if an invalid key is included in parameters.
            TypeError if a value in parameters has an invalid type.

        """
        super().__init__(PARAMS["command"], PARAMS["required_parameters"], PARAMS["optional_parameters"])
        self.check_parameters(parameters)
        self.remove_names = parameters['remove_names']
        ignore_missing = parameters['ignore_missing']
        if ignore_missing:
            self.error_handling = 'ignore'
        else:
            self.error_handling = 'raise'

    def do_op(self, df):
        """ Remove indicated columns from a dataframe.

        Args:
            df (DataFrame) - The DataFrame whose columns are to be removed.

        Raises:
            KeyError if ignore_missing is false and column not in df is to be removed.

        """

        return df.drop(self.remove_names, axis=1, errors=self.error_handling)
