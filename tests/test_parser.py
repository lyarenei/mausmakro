import unittest

from mausmakro.lib.enums import Opcode
from mausmakro.lib.exceptions import LabelException, ParserException, \
    PreprocessorException
from mausmakro.lib.types import Command
from mausmakro.parsing import Parser
from mausmakro.preprocessor import Preprocessor


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

    @unittest.skip("Label command is not supported yet")
    def test_duplicate_label(self):
        filename = 'test_macros/duplicate_label.txt'
        file_content = Preprocessor(filename).process()
        parser = Parser(filename, file_content)
        parser.parse()
        self.assertRaises(ParserException, parser.perform_checks)

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
