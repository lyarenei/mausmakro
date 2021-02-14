import unittest

from lark import Token

from parsing import Parser


class TestParseToken(unittest.TestCase):

    def test_parse_token_name(self):
        res = Parser.parse_token(Token('NAME', 'foobar'))
        self.assertEqual(res, 'foobar')

    def test_parse_token_file(self):
        res = Parser.parse_token(Token('FILE', 'image.jpg'))
        self.assertEqual(res, 'image.jpg')

    def test_parse_token_coords(self):
        res = Parser.parse_token(Token('COORDS', '1,1'))
        self.assertTupleEqual(res, (1, 1))

    def test_parse_token_time_s(self):
        res = Parser.parse_token(Token('TIME', '50s'))
        self.assertEqual(res, 50)

    def test_parse_token_time_m(self):
        res = Parser.parse_token(Token('TIME', '42m'))
        self.assertEqual(res, 2520)

    def test_parse_token_time_h(self):
        res = Parser.parse_token(Token('TIME', '12h'))
        self.assertEqual(res, 43200)

    def test_parse_token_invalid(self):
        self.assertRaises(
            NotImplementedError, Parser.parse_token, Token('FOO', '10s'))
