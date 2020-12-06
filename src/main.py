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
@click.option('--macro', '-m', help="Name of the macro to interpret")
@click.option('--times', '-t', type=int, default=-1,
              help="Number of times to repeat specified macro, "
                   "defaults to -1 (infinite")
@click.option('--go-back-on-fail', is_flag=True,
              help="Go back to previous command on current command failure"
                   "(i.e.: click wasn't processed by the application "
                   "so image is not found -> go back and click again).")
def interpret(file, macro, times, go_back_on_fail):
    opts = {
        'file': file,
        'go_back_on_fail': go_back_on_fail
    }

    try:
        instructions, label_table = Parser(file).parse()

    except ParserException as e:
        print(f"An error occurred while parsing the file:\n{e}")
        sys.exit(1)

    interpreter = Interpreter(instructions, label_table, opts)
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
