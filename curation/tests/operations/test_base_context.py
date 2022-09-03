import os
import unittest
from curation import RemoveRowsOp, Dispatcher
from curation.remodeling.operations.base_context import BaseContext


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_root = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data'))

    @classmethod
    def tearDownClass(cls):
        pass

    def test_constructor(self):
        base_con = BaseContext('temp_type', 'temp_name', 'temp_path')
        self.assertIsInstance(base_con, BaseContext, 'constructor creates a BaseContext object')

    def test_get_summary(self):
        base_con = BaseContext('temp_type', 'temp_name', 'temp_path')
        summary1 = base_con.get_summary()
        self.assertIsInstance(summary1, dict, "get_summary returns a dictionary by default")
        summary2 = base_con.get_summary(as_json=True)
        self.assertIsInstance(summary2, str, "get_summary returns a dictionary if json requested")
        summary3 = base_con.get_text_summary(verbose=False)
        self.assertIsInstance(summary3, str, "get_text_summary returns a str if verbose is False")
        summary4 = base_con.get_text_summary()
        self.assertIsInstance(summary4, str, "get_text_summary returns a str by default")
        summary5 = base_con.get_text_summary(verbose=True)
        self.assertIsInstance(summary5, str, "get_text_summary returns a str with verbose True")
        self.assertEqual(summary4, summary5, "get_text_summary string is same when verbose omitted or True")


if __name__ == '__main__':
    unittest.main()
