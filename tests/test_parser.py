import unittest
from unittest import mock
from unittest.mock import patch

from mausmakro.lib.enums import Opcode
from mausmakro.lib.exceptions import LabelException, ParserException, \
    PreprocessorException
from mausmakro.lib.types import Command, Conditional
from mausmakro.parsing import Parser
from mausmakro.preprocessor import Preprocessor


def mock_generate_label(_):
    mock_generate_label.cnt += 1
    return f'fbartest_{mock_generate_label.cnt}'


mock_generate_label.cnt = 0


class TestParser(unittest.TestCase):

    def test_comments(self):
        filename = 'test_macros/comments.txt'
        file_content = Preprocessor(filename).process()
        ins, labels = Parser(filename, file_content).parse()

        expected_labels = {'foobar': 0}
        expected_ins = [
            Command(Opcode.LABEL, 'foobar'),
            Command(Opcode.WAIT, 1),
            Command(Opcode.END),
        ]

        self.assertListEqual(ins, expected_ins)
        self.assertDictEqual(labels, expected_labels)

    @mock.patch('mausmakro.parsing.Parser._generate_label')
    def test_conditional(self, _generate_label):
        _generate_label.return_value = 'fbartest'

        filename = 'test_macros/conditional.txt'
        file_content = Preprocessor(filename).process()
        ins, labels = Parser(filename, file_content).parse()

        cond = Conditional(Opcode.IF)
        cond.condition = Command(Opcode.FIND, ('image.png', 5))
        cond.end_label = 'fbartest'
        cond.else_label = None

        expected_labels = {'foobar': 0, cond.end_label: 3}
        expected_ins = [
            Command(Opcode.LABEL, 'foobar'),
            cond,
            Command(Opcode.WAIT, 4),
            Command(Opcode.LABEL, cond.end_label),
            Command(Opcode.END),
        ]

        self.assertListEqual(ins, expected_ins)
        self.assertDictEqual(labels, expected_labels)

    @patch.object(Parser, '_generate_label', mock_generate_label)
    def test_conditional_else(self):
        filename = 'test_macros/conditional_else.txt'
        file_content = Preprocessor(filename).process()
        ins, labels = Parser(filename, file_content).parse()

        cond = Conditional(Opcode.IF)
        cond.condition = Command(Opcode.FIND, ('image.png', 5))
        cond.end_label = 'fbartest_1'
        cond.else_label = 'fbartest_2'

        expected_labels = {'foobar': 0, cond.else_label: 4, cond.end_label: 6}
        expected_ins = [
            Command(Opcode.LABEL, 'foobar'),
            cond,
            Command(Opcode.WAIT, 4),
            Command(Opcode.JUMP, cond.end_label),
            Command(Opcode.LABEL, cond.else_label),
            Command(Opcode.WAIT, 5),
            Command(Opcode.LABEL, cond.end_label),
            Command(Opcode.END),
        ]

        self.assertListEqual(ins, expected_ins)
        self.assertDictEqual(labels, expected_labels)

    def test_duplicate_label(self):
        filename = 'test_macros/duplicate_label.txt'
        file_content = Preprocessor(filename).process()
        parser = Parser(filename, file_content)
        self.assertRaises(ParserException, parser.parse)

    def test_duplicate_macro(self):
        filename = 'test_macros/duplicate_macros.txt'
        file_content = Preprocessor(filename).process()
        parser = Parser(filename, file_content)
        self.assertRaises(ParserException, parser.parse)

    def test_empty(self):
        filename = 'test_macros/empty.txt'
        file_content = Preprocessor(filename).process()
        self.assertRaises(ParserException, Parser, filename, file_content)

    def test_empty_macro(self):
        filename = 'test_macros/empty_macro.txt'
        file_content = Preprocessor(filename).process()
        self.assertRaises(ParserException, Parser, filename, file_content)

    def test_import_statement(self):
        filename = 'test_macros/import_statement.txt'
        file_content = Preprocessor(filename).process()
        ins, labels = Parser(filename, file_content).parse()

        expected_labels = {'foobar': 0, 'foobaz': 4}
        expected_ins = [
            Command(Opcode.LABEL, 'foobar'),
            Command(Opcode.WAIT, 1),
            Command(Opcode.CLICK, (1, 1)),
            Command(Opcode.END),
            Command(Opcode.LABEL, 'foobaz'),
            Command(Opcode.WAIT, 1),
            Command(Opcode.END),
        ]

        self.assertListEqual(ins, expected_ins)
        self.assertDictEqual(labels, expected_labels)

    def test_import_statement_invalid(self):
        filename = 'test_macros/import_statement_invalid.txt'
        preprocessor = Preprocessor(filename)
        self.assertRaises(PreprocessorException, preprocessor.process)

    def test_indents_newlines(self):
        filename = 'test_macros/indents_newlines.txt'
        file_content = Preprocessor(filename).process()
        ins, labels = Parser(filename, file_content).parse()

        expected_labels = {'foobar': 0}
        expected_ins = [
            Command(Opcode.LABEL, 'foobar'),
            Command(Opcode.WAIT, 5),
            Command(Opcode.JUMP, 'foobar'),
            Command(Opcode.END),
        ]

        self.assertListEqual(ins, expected_ins)
        self.assertDictEqual(labels, expected_labels)

    def test_invalid_name(self):
        filename = 'test_macros/invalid_name.txt'
        file_content = Preprocessor(filename).process()
        self.assertRaises(ParserException, Parser, filename, file_content)

    def test_procedure(self):
        filename = 'test_macros/procedure.txt'
        file_content = Preprocessor(filename).process()
        ins, labels = Parser(filename, file_content).parse()

        expected_labels = {'foo': 0}
        expected_ins = [
            Command(Opcode.LABEL, 'foo'),
            Command(Opcode.CLICK, (1, 1)),
            Command(Opcode.RETURN),
        ]

        self.assertListEqual(ins, expected_ins)
        self.assertDictEqual(labels, expected_labels)

    def test_valid_name(self):
        filename = 'test_macros/valid_name.txt'
        file_content = Preprocessor(filename).process()
        ins, labels = Parser(filename, file_content).parse()

        expected_labels = {'fO0-bA_r': 0}
        expected_ins = [
            Command(Opcode.LABEL, 'fO0-bA_r'),
            Command(Opcode.WAIT, 1),
            Command(Opcode.END),
        ]

        self.assertListEqual(ins, expected_ins)
        self.assertDictEqual(labels, expected_labels)

    def test_undefined_label(self):
        filename = 'test_macros/undefined_label.txt'
        file_content = Preprocessor(filename).process()
        parser = Parser(filename, file_content)
        parser.parse()
        self.assertRaises(LabelException, parser.perform_checks)
