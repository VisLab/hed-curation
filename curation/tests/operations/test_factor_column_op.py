import json
import pandas as pd
import numpy as np
import unittest
from curation.remodeling.operations.factor_column_op import FactorColumnOp


class Test(unittest.TestCase):
    """

    TODO: Test when no factor names and values are given.

    """
    @classmethod
    def setUpClass(cls):
        cls.sample_data = [[0.0776, 0.5083, 'go', 'n/a', 0.565, 'correct', 'right', 'female'],
                           [5.5774, 0.5083, 'unsuccesful_stop', 0.2, 0.49, 'correct', 'right', 'female'],
                           [9.5856, 0.5084, 'go', 'n/a', 0.45, 'correct', 'right', 'female'],
                           [13.5939, 0.5083, 'succesful_stop', 0.2, 'n/a', 'n/a', 'n/a', 'female'],
                           [17.1021, 0.5083, 'unsuccesful_stop', 0.25, 0.633, 'correct', 'left', 'male'],
                           [21.6103, 0.5083, 'go', 'n/a', 0.443, 'correct', 'left', 'male']]
        cls.factored = [[0.0776, 0.5083, 'go', 'n/a', 0.565, 'correct', 'right', 'female', 0, 0],
                        [5.5774, 0.5083, 'unsuccesful_stop', 0.2, 0.49, 'correct', 'right', 'female', 0, 1],
                        [9.5856, 0.5084, 'go', 'n/a', 0.45, 'correct', 'right', 'female', 0, 0],
                        [13.5939, 0.5083, 'succesful_stop', 0.2, 'n/a', 'n/a', 'n/a', 'female', 1, 0],
                        [17.1021, 0.5083, 'unsuccesful_stop', 0.25, 0.633, 'correct', 'left', 'male', 0, 1],
                        [21.6103, 0.5083, 'go', 'n/a', 0.443, 'correct', 'left', 'male', 0, 0]]
        cls.sample_columns = ['onset', 'duration', 'trial_type', 'stop_signal_delay', 'response_time',
                              'response_accuracy', 'response_hand', 'sex']
        base_parameters = {
            "column_name": "trial_type",
            "factor_values": ["succesful_stop", "unsuccesful_stop"],
            "factor_names": ["stopped", "stop_failed"]
        }
        cls.default_factor_columns = ["trial_type.succesful_stop", "trial_type.unsuccesful_stop"]
        cls.json_parms = json.dumps(base_parameters)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_valid_factors_no_extras(self):
        # Test correct when all valid and no unwanted information
        parms = json.loads(self.json_parms)
        op = FactorColumnOp(parms)
        df = pd.DataFrame(self.sample_data, columns=self.sample_columns)
        df_check = pd.DataFrame(self.factored, columns=self.sample_columns + parms['factor_names'])
        df_test = pd.DataFrame(self.sample_data, columns=self.sample_columns)
        df_new = op.do_op(None, df_test, 'sample_data')
        self.assertEqual(len(df_check), len(df_new),
                         "factor_column should not change number of rows with ignore missing")
        self.assertEqual(len(df_check.columns), len(df.columns) + len(parms["factor_values"]),
                         "factor_column check should have extra columns with no extras and ignore missing")
        self.assertTrue(list(df_new.columns) == list(df_check.columns),
                        "factor_column resulting df should have correct columns with no extras and ignore missing")
        self.assertTrue(np.array_equal(df_new.to_numpy(), df_check.to_numpy()),
                        "factor_column should have expected values when no extras and ignore missing")

        # Test that df has not been changed by the op
        self.assertTrue(list(df.columns) == list(df_test.columns),
                        "factor_column should not change the input df columns when no extras and ignore missing")
        self.assertTrue(np.array_equal(df.to_numpy(), df_test.to_numpy()),
                        "factor_column should not change the input df values when no extras and ignore missing")

    def test_valid_factors_no_extras_no_ignore(self):
        # Test when no extras and extras not ignored.
        parms = json.loads(self.json_parms)
        op = FactorColumnOp(parms)
        df = pd.DataFrame(self.sample_data, columns=self.sample_columns)
        df_check = pd.DataFrame(self.factored, columns=self.sample_columns + parms['factor_names'])
        df_test = pd.DataFrame(self.sample_data, columns=self.sample_columns)
        df_new = op.do_op(None, df_test, 'sample_data')
        self.assertEqual(len(df_check), len(df_new),
                         "factor_column should not change number of rows with no extras and no ignore")
        self.assertEqual(len(df_check.columns), len(df.columns) + len(parms["factor_values"]),
                         "factor_column check should have extra columns with no extras and no ignore")
        self.assertTrue(list(df_new.columns) == list(df_check.columns),
                        "factor_column resulting df should have correct columns with no extras and no ignore")
        self.assertTrue(np.array_equal(df_new.to_numpy(), df_check.to_numpy()),
                        "factor_column should have expected values when no extras and no ignore")

        # Test that df has not been changed by the op
        self.assertTrue(list(df.columns) == list(df_test.columns),
                        "factor_column should not change the input df columns when no extras and no ignore missing")
        self.assertTrue(np.array_equal(df.to_numpy(), df_test.to_numpy()),
                        "factor_column should not change the input df values when no extras and no ignore missing")

    def test_valid_factors_extras_ignore(self):
        # Test when extra factor values but ignored
        parms = json.loads(self.json_parms)
        df = pd.DataFrame(self.sample_data, columns=self.sample_columns)
        df_check = pd.DataFrame(self.factored, columns=self.sample_columns + parms['factor_names'])
        parms["factor_values"] = ["succesful_stop", "unsuccesful_stop", "face"]
        parms["factor_names"] = ["stopped", "stop_failed", "baloney"]
        op = FactorColumnOp(parms)
        df_check["baloney"] = [0, 0, 0, 0, 0, 0]
        df_test = pd.DataFrame(self.sample_data, columns=self.sample_columns)
        df_new = op.do_op(None, df_test, 'sample_data')
        self.assertEqual(len(df_check), len(df_new),
                         "factor_column should not change number of rows with extras and ignore missing")
        self.assertEqual(len(df_check.columns), len(df.columns) + len(parms["factor_values"]),
                         "factor_column check should have extra columns with extras and ignore missing")
        self.assertEqual(len(df_check.columns), len(df.columns) + len(parms["factor_values"]),
                         "factor_column should have extra columns with extras and ignore missing")
        self.assertTrue(list(df_new.columns) == list(df_check.columns),
                        "factor_column resulting df should have correct columns with extras and ignore missing")
        self.assertTrue(np.array_equal(df_new.to_numpy(), df_check.to_numpy()),
                        "factor_column should have expected values with extras and ignore missing")

        # Test that df has not been changed by the op
        self.assertTrue(list(df.columns) == list(df_test.columns),
                        "factor_column should not change the input df columns when extras and no ignore missing")
        self.assertTrue(np.array_equal(df.to_numpy(), df_test.to_numpy()),
                        "factor_column should not change the input df values when extras and no ignore missing")

    def test_valid_factors_extras_no_ignore(self):
        # Test when extra factors are included but not ignored.
        parms = json.loads(self.json_parms)
        df = pd.DataFrame(self.sample_data, columns=self.sample_columns)
        df_check = pd.DataFrame(self.factored, columns=self.sample_columns + parms['factor_names'])
        parms["factor_values"] = ["succesful_stop", "unsuccesful_stop", "face"]
        parms["factor_names"] = ["stopped", "stop_failed", "baloney"]
        op = FactorColumnOp(parms)
        df_check["baloney"] = [0, 0, 0, 0, 0, 0]
        df_test = pd.DataFrame(self.sample_data, columns=self.sample_columns)
        df_new = op.do_op(None, df_test, 'sample_data')
        self.assertEqual(len(df_check), len(df_new),
                         "factor_column should not change number of rows with extras and ignore missing")
        self.assertEqual(len(df_check.columns), len(df.columns) + len(parms["factor_values"]),
                         "factor_column check should have extra columns with extras and ignore missing")
        self.assertEqual(len(df_check.columns), len(df.columns) + len(parms["factor_values"]),
                         "factor_column should have extra columns with extras and ignore missing")
        self.assertTrue(list(df_new.columns) == list(df_check.columns),
                        "factor_column resulting df should have correct columns with extras and ignore missing")
        self.assertTrue(np.array_equal(df_new.to_numpy(), df_check.to_numpy()),
                        "factor_column should have expected values with extras and ignore missing")

        # Test that df has not been changed by the op
        self.assertTrue(list(df.columns) == list(df_test.columns),
                        "factor_column should not change the input df columns when extras and no ignore missing")
        self.assertTrue(np.array_equal(df.to_numpy(), df_test.to_numpy()),
                        "factor_column should not change the input df values when extras and no ignore missing")


if __name__ == '__main__':
    unittest.main()
