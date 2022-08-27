import json


class BaseContext:

    def __init__(self, context_type, context_name, context_filename):
        self.context_type = context_type
        self.context_name = context_name
        self.context_filename = context_filename

    def get_summary(self, as_json=False):
        summary = {'context_name': self.context_name, 'context_type': self.context_type,
                   'context_filename': self.context_filename}
        if as_json:
            return json.dumps(summary, indent=4)
        else:
            return summary

    def get_text_summary(self, title='', verbose=True):
        summary = self.get_summary(as_json=False)
        sum_str = []
        if title:
            sum_str = [title]
        if verbose:
            extra_info = ["Details should be included if verbose is True"]
        else:
            extra_info = []
        sum_str = sum_str + \
            [f"Context name: {summary['context_name']}", f"Context type: {summary['context_type']}",
             f"Context filename: {summary['context_filename']}"] + extra_info
        return '\n'.join(sum_str)
