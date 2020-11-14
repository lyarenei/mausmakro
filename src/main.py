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
@click.option('--output', default="mausmakro_saved")
def record(output):
    rec = Recorder(output)
    rec.record()


@main.command()
@click.argument('file')
@click.argument('macro')
@click.argument('times', type=int)
def interpret(file, macro, times):
    parser = Lark(ebnf, parser='lalr')
    with open(file, 'r') as f:
        source = f.read()

    tree = parser.parse(source)
    interpreter = Interpreter(tree)
    interpreter.interpret(macro, repeats=times)


if __name__ == '__main__':
    main()
