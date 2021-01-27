#!/usr/local/bin/python3
import sys

import click

from parsing import Parser
from preprocessor import Preprocessor
from recorder import Recorder
from ui import Ui


@click.group()
def main():
    pass


@main.command()
@click.option('--output', '-o', default=None,
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
@click.option('--enable-retry', is_flag=True,
              help="Enable command retrying before going back "
                   "(with --go-back-on-fail) or failing completely.")
@click.option('--retry-times', type=click.IntRange(1, None), default=1,
              help="Retry the failing command specified times before failing. "
                   "Defaults to 1. Has no effect if --retry-times command "
                   "is not specified")
@click.option('--color-match', is_flag=True,
              help="Perform color image find by default")
@click.option('--match-step', type=click.IntRange(1, 5), default=2,
              help="Image match step. Higher value means faster search, "
                   "but lowers accuracy. Recommended for higher res (>1080p) "
                   "displays. Defaults to 2.")
@click.option('--pause-on-fail', is_flag=True,
              help="Pause execution if current instruction fails, "
                   "instead of exiting.")
def interpret(file: str, macro: str, times: int, enable_retry: bool,
              retry_times: int, color_match: bool, match_step: int,
              pause_on_fail: bool):

    opts = {
        'color_match': color_match,
        'enable_retry': enable_retry,
        'file': file,
        'match_step': match_step,
        'retry_times': retry_times,
        'pause_on_fail': pause_on_fail
    }

    try:
        file_content = Preprocessor(file).process()
        parser = Parser(file, file_content)
        instructions, label_table = parser.parse()
        parser.perform_checks()

    except Exception as e:
        print(f"An error occurred while parsing the file:\n{e}")
        sys.exit(1)

    program = Ui()
    program.start(macro, times, instructions, label_table, opts)


if __name__ == '__main__':
    main()
