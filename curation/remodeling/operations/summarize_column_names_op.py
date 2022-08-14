from curation.remodeling.operations.base_op import BaseOp


PARAMS = {
    "command": "summarize_column_names",
    "required_parameters": {
        "summary_name": str,
        "summary_path": str
    },
    "optional_parameters": {}
}


class SummarizeColumnNamesOp(BaseOp):
    """ Creates factor columns corresponding to values in specified column.

        Notes: The required parameters are:
            - column_name (string)  The name of a column in the DataRrame.
            - factor_values (list)  Values in the column column_name to create factors for.
            - factor_names (list)   Names to use as the factor columns.

    """

    def __init__(self, parameters):
        super().__init__(PARAMS["command"], PARAMS["required_parameters"], PARAMS["optional_parameters"])
        self.check_parameters(parameters)
        self.summary_name = parameters['summary_name']
        self.summary_path = parameters['summary_path']
        self.summary_info = {}

    def do_op(self, dispatcher, df, name, sidecar=None):
        """ Create factor columns corresponding to values in a specified column.

        Args:
            dispatcher (Dispatcher) - dispatcher object for context
            df (DataFrame) - The DataFrame to be remodeled.
            name (str) - Unique identifier for the dataframe -- often the original file path.
            sidecar (Sidecar or file-like)   Only needed for HED operations

        Returns:
            DataFrame - a new DataFrame with the factor columns appended.

        """

        factor_values = self.factor_values
        factor_names = self.factor_names
        if len(factor_values) == 0:
            factor_values = df[self.column_name].unique()
            factor_names = [self.column_name + '.' + str(column_value) for column_value in factor_values]

        df_new = df.copy()
        for index, factor_value in enumerate(factor_values):
            factor_index = df_new[self.column_name].map(str).isin([str(factor_value)])
            column = factor_names[index]
            df_new[column] = factor_index.astype(int)
        return df_new
