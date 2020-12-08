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
@click.option('--enable-retry', is_flag=True,
              help="Enable command retrying before going back "
                   "(with --go-back-on-fail) or failing completely.")
@click.option('--retry-times', type=click.IntRange(1, None), default=1,
              help="Retry the failing command specified times before failing. "
                   "Defaults to 1. Has no effect if --retry-times command "
                   "is not specified")
def interpret(file: str, macro: str, times: int, go_back_on_fail: bool,
              enable_retry: bool, retry_times: int):
    opts = {
        'file': file,
        'go_back_on_fail': go_back_on_fail,
        'enable_retry': enable_retry,
        'retry_times': retry_times
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
