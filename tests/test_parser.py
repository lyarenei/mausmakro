import unittest

from lib.enums import Opcode
from lib.exceptions import ParserException
from lib.types import Command
from parsing import Parser
from preprocessor import Preprocessor


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
        parser = Parser(filename, file_content)
        parser.parse()
        self.assertRaises(ParserException, parser.perform_checks)

    def test_empty_macro(self):
        filename = 'test_macros/empty_macro.txt'
        file_content = Preprocessor(filename).process()
        parser = Parser(filename, file_content)
        parser.parse()
        self.assertRaises(ParserException, parser.perform_checks)

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
        file_content = Preprocessor(filename).process()
        parser = Parser(filename, file_content)
        parser.parse()
        self.assertRaises(ParserException, parser.perform_checks)

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

    def test_procedure(self):
        filename = 'test_macros/procedure.txt'
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

    def test_undefined_label(self):
        filename = 'test_macros/undefined_label.txt'
        file_content = Preprocessor(filename).process()
        parser = Parser(filename, file_content)
        parser.parse()
        self.assertRaises(ParserException, parser.perform_checks)
