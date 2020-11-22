#!/usr/local/bin/python3

import click
from lark import Lark

from definitions.ebnf import ebnf
from interpreter import Interpreter
from recorder import Recorder


@click.group()
def main():
    pass


@main.command()
@click.option('--output', '-o', default="mausmakro_saved",
              help="Output file")
def record(output):
    rec = Recorder(output)
    rec.record()


@main.command()
@click.option('--file', '-f', help="Source file with macros")
@click.option('--macro', '-m',
              help="Name of the macro to interpret")
@click.option('--times', '-t', type=int, default=-1,
              help="Number of times to repeat specified macro, "
                   "defaults to -1 (infinite")
def interpret(file, macro, times):
    parser = Lark(ebnf, parser='lalr')
    with open(file, 'r') as f:
        source = f.read()

    tree = parser.parse(source)
    interpreter = Interpreter(tree)
    interpreter.interpret(macro, repeats=times)


if __name__ == '__main__':
    main()
