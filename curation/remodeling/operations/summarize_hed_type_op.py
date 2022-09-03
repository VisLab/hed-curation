import json
from hed import TabularInput
from hed.tools import get_assembled_strings, HedTypeVariable, HedVariableManager, HedVariableSummary
from curation.remodeling.operations.base_op import BaseOp
from curation.remodeling.operations.base_context import BaseContext


PARAMS = {
    "command": "summarize_hed_type",
    "required_parameters": {
        "summary_name": str,
        "summary_filename": str,
        "type_tag": str,
    },
    "optional_parameters": {
    }
}


class SummarizeHedTypeOp(BaseOp):
    """ Summarize the occurrences of a type tag in the dataset.

    Notes: The required parameters are:
        - summary_name (str)   The name of the summary.
        - summary_filename (str)   Base filename of the summary.
        - type_tag (str)  Type tag to summarize (e.g. 'condition-variable' or 'task')

    The purpose of this op is to produce a summary of the occurrences of specified tag. This summary
    is often used with 'condition-variable' to produce a summary of the experimental design.


    """

    def __init__(self, parameters):
        super().__init__(PARAMS["command"], PARAMS["required_parameters"], PARAMS["optional_parameters"])
        self.check_parameters(parameters)
        self.summary_type = 'summarize_hed_type'
        self.summary_name = parameters['summary_name']
        self.summary_filename = parameters['summary_filename']
        self.type_tag = parameters['type_tag'].lower()

    def do_op(self, dispatcher, df, name, sidecar=None, verbose=False):
        """ Create factor columns corresponding to values in a specified column.

        Args:
            dispatcher (Dispatcher) - dispatcher object for context
            df (DataFrame) - The DataFrame to be remodeled.
            name (str) - Unique identifier for the dataframe -- often the original file path.
            sidecar (Sidecar or file-like)   Only needed for HED operations.
            verbose (bool) If True output informative messages during operation.

        Returns:
            DataFrame - a new DataFrame with the factor columns appended.

        Side-effect:
            Updates the context

        """

        summary = dispatcher.context_dict.get(self.summary_name, None)
        if not summary:
            summary = HedTypeSummary(self)
            dispatcher.context_dict[self.summary_name] = summary
        input_data = TabularInput(df, hed_schema=dispatcher.hed_schema, sidecar=sidecar)
        hed_strings = get_assembled_strings(input_data, hed_schema=dispatcher.hed_schema, expand_defs=False)
        definitions = input_data.get_definitions().gathered_defs
        var_manager = HedVariableManager(hed_strings, dispatcher.hed_schema, definitions)
        var_manager.add_type_variable(self.type_tag)
        var_map = var_manager.get_type_variable(self.type_tag)
        summary.update_context(var_map)
        return df


class HedTypeSummary(BaseContext):

    def __init__(self, sum_op):
        super().__init__(sum_op.summary_type, sum_op.summary_name, sum_op.summary_filename)
        self.variable_type = sum_op.type_tag
        self.summary = HedVariableSummary(variable_type=sum_op.type_tag)

    def update_context(self, type, var_map):
        if type == self.variable_type:
            self.summary.update_summary(var_map)

    def get_summary(self, as_json=False, verbose=True):
        summary = super().get_summary(as_json=False, verbose=verbose)
        summary['summary'] = self.summary.get_summary()
        if as_json:
            return json.dumps(summary, indent=4)
        else:
            return summary

    def get_text_summary(self, title='', verbose=True):
        sum_str = super().get_text_summary(title=title, verbose=verbose)
        return sum_str + '\n' + self.get_summary(as_json=True, verbose=verbose).replace('"', '')
