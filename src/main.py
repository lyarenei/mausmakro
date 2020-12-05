#!/usr/local/bin/python3
import sys

import click

from definitions.exceptions import ParserException
from interpreter import Interpreter
from parser import Parser
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
    try:
        instructions, label_table = Parser(file).parse()

    except ParserException as e:
        print(f"An error occurred while parsing the file:\n{e}")
        sys.exit(1)

    interpreter = Interpreter(instructions, label_table, file)
    iters = 0

    while iters < times or times == -1:
        try:
            interpreter.interpret(macro)

        except Exception as e:
            print(f"An error occurred when interpreting the macro:\n{e}")
            sys.exit(2)

        iters += 1


if __name__ == '__main__':
    main()
