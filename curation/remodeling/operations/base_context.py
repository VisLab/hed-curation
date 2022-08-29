import json
import os


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

    def get_text_summary(self, verbose=True):
        summary = [f"Context name: {self.context_name}", f"Context type: {self.context_type}",
                   f"Context filename: {self.context_filename}", self.get_summary(as_json=False)]
        return 'n'.join(summary)

    def save(self, save_dir, file_formats, verbose=True):
        if not file_formats:
            return
        file_base = os.path.join(save_dir, self.context_filename)
        for file_format in file_formats:
            if file_format == '.txt':
                summary = self.get_text_summary(verbose=verbose)
            elif file_format == '.json':
                summary = self.get_summary(as_json=True)
            else:
                continue

            with open(os.path.realpath(file_base + file_format), 'w') as text_file:
                text_file.write(summary)
