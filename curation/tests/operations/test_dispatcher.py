import os
import json
import unittest
import numpy as np
import pandas as pd
from curation import Dispatcher
from curation.remodeling.operations.base_op import BaseOp


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_path = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data'))
        cls.sample_data = [[0.0776, 0.5083, 'go', 'n/a', 0.565, 'correct', 'right', 'female'],
                           [5.5774, 0.5083, 'unsuccesful_stop', 0.2, 0.49, 'correct', 'right', 'female'],
                           [9.5856, 0.5084, 'go', 'n/a', 0.45, 'correct', 'right', 'female'],
                           [13.5939, 0.5083, 'succesful_stop', 0.2, 'n/a', 'n/a', 'n/a', 'female'],
                           [17.1021, 0.5083, 'unsuccesful_stop', 0.25, 0.633, 'correct', 'left', 'male'],
                           [21.6103, 0.5083, 'go', 'n/a', 0.443, 'correct', 'left', 'male']]
        cls.sample_columns = ['onset', 'duration', 'trial_type', 'stop_signal_delay', 'response_time',
                              'response_accuracy', 'response_hand', 'sex']


    @classmethod
    def tearDownClass(cls):
        pass

    def test_parse_commands_empty(self):
        command_list = []
        commands, errors = Dispatcher.parse_commands(command_list)
        self.assertFalse(commands, "parse_commands for empty command list is empty")
        self.assertFalse(errors, "parse_commands for empty command list does not produce errors")

    def test_parse_commands_no_command(self):
        test = [{"command": "remove_rows", "parameters": {"column_name": "response_time", "remove_values": ["n/a"]}},
                {"parameters": {"column_name": "trial_type", "remove_values": ["succesful_stop", "unsuccesful_stop"]}}]
        commands, errors = Dispatcher.parse_commands(test)
        self.assertFalse(commands, "parse_commands returns empty if no command")
        self.assertEqual(len(errors), 1, "parse_command returns a list of one error if one command with no command")
        self.assertEqual(errors[0]['index'], 1, "parse_command error has the correct index for missing command")
        self.assertEqual(errors[0]['error_type'], KeyError,
                         "parse_command error has the correct type for missing command")

    def test_parse_commands_no_parameters(self):
        test = [{"command": "remove_rows", "parameters": {"column_name": "response_time", "remove_values": ["n/a"]}},
                {"command": "remove_rows"}]
        commands, errors = Dispatcher.parse_commands(test)
        self.assertFalse(commands, "parse_commands returns empty if no parameters")
        self.assertEqual(len(errors), 1, "parse_command returns a list of one error if one command with no parameters")
        self.assertEqual(errors[0]['index'], 1, "parse_command error has the correct index for missing parameters")
        self.assertEqual(errors[0]['error_type'], KeyError,
                         "parse_command error has the correct type for missing parameters")

    def test_parse_commands_missing_required(self):
        test = [{"command": "remove_rows",
                 "parameters": {"column_name": "trial_type", "remove_values": ["succesful_stop", "unsuccesful_stop"]}},
                {"command": "remove_rows", "parameters": {"column_name": "response_time"}}]
        commands, errors = Dispatcher.parse_commands(test)
        self.assertFalse(commands, "parse_commands returns empty if missing required")
        self.assertEqual(len(errors), 1,
                         "parse_command returns a list of one error if one command with missing required")
        self.assertEqual(errors[0]['index'], 1, "parse_command error has the correct index for missing parameters")
        self.assertEqual(errors[0]['error_type'], KeyError,
                         "parse_command error has the correct type for missing required")

    def test_dispatch_command_list(self):
        test = [{"command": "remove_rows",
                 "parameters": {"column_name": "trial_type", "remove_values": ["succesful_stop", "unsuccesful_stop"]}},
                {"command": "remove_rows", "parameters": {"column_name": "response_time", "remove_values": ["n/a"]}}]
        dispatch = Dispatcher(test)
        com_list = dispatch.command_list
        self.assertEqual(len(com_list), len(test), "dispatch has a command for each item in command list")
        for item in com_list:
            self.assertIsInstance(item, BaseOp)

    def test_dispatcher_constructor(self):
        model_path1 = os.path.join(self.data_path, 'simple_reorder_remdl.json')
        with open(model_path1) as fp:
            model1 = json.load(fp)
        dispatch = Dispatcher(model1)
        self.assertEqual(len(dispatch.command_list), len(model1),
                         "dispatcher command list should have one item for each command")

    def test_dispatcher_run_operations(self):
        model_path1 = os.path.join(self.data_path, 'simple_reorder_remdl.json')
        with open(model_path1) as fp:
            model1 = json.load(fp)
        dispatch = Dispatcher(model1)
        df_test = pd.DataFrame(self.sample_data, columns=self.sample_columns)
        num_test_rows = len(df_test)
        df_test_values = df_test.to_numpy()
        df_new = dispatch.run_operations(df_test)
        reordered_columns = ["onset", "duration", "trial_type", "response_time"]
        self.assertTrue(reordered_columns == list(df_new.columns),
                        "run_operations resulting df should have correct columns")
        self.assertTrue(list(df_test.columns) == self.sample_columns,
                        "run_operations did not change the input df columns")
        self.assertEqual(len(df_test), num_test_rows, "run_operations did not change the input df rows")
        self.assertFalse(np.array_equal(df_test_values, df_test.to_numpy),
                         "run_operations does not change the values in the input df")
        self.assertEqual(len(df_new), num_test_rows, "run_operations did not change the number of output rows")
        self.assertEqual(len(dispatch.command_list), len(model1),
                         "dispatcher command list should have one item for each command")


if __name__ == '__main__':
    unittest.main()
