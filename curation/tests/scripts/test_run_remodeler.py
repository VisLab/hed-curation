import os
import subprocess
import json
import unittest
import numpy as np
import pandas as pd
from curation import Dispatcher
from curation.remodeling.scripts import run_remodel
from curation.remodeling.operations.base_op import BaseOp


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.script_path = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                        '../../remodeling/scripts/'))

    @classmethod
    def tearDownClass(cls):
        pass

    def test_run_parse_commands(self):
        try:
            command_file = os.path.realpath(os.path.join(self.script_path, 'run_remodel.py'))
            # result = subprocess.run(['python', command_file, "-d",  "temp"],
            #                         check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as error:
            print(error.stdout)
            print(error.stderr)
            raise error


if __name__ == '__main__':
    unittest.main()
