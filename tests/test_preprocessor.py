import unittest

from mausmakro.lib.exceptions import PreprocessorException
from preprocessor import Preprocessor


class TestPreprocessor(unittest.TestCase):

    def test_import_statement(self):
        filename = 'test_macros/import_statement.txt'
        content = Preprocessor(filename).process()
        expected_content = "MACRO foobar {\n    WAIT 1s\n    CLICK 1,1\n}\n" \
                           "MACRO foobaz {\n  WAIT 1s\n}\n"
        self.assertEqual(content, expected_content)

    def test_import_statement_invalid(self):
        filename = 'test_macros/import_statement_invalid.txt'
        preprocessor = Preprocessor(filename)
        with self.assertRaises(PreprocessorException):
            preprocessor.process()
