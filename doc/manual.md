# Manual

Mausmakro has four modes, each of which have additional parameters described in
following sections.

## Interpreter mode

The main mode. Interpret the specified macro from a file.

- `--file`, `-f` <file>
    - The macro source file in which is the macro to be interpreted.

- `--macro`, `-m` <name>
    - The name of the macro to be interpreted.

- `--times`, `-t` <times>
    - How many times to repeat the macro. If not specified, the macro is
      interpreted in an infinite loop.

- `--enable-retry`
    - Enable command retrying before failing completely.

- `--retry-times` <number>
    - Retry the failing command specified times before failing. Defaults to 1.
      Has no effect if `--retry-times` flag is not specified.

- `--color-match`
    - Perform color image detection instead of grayscale. Can lower speed of
      image detection. Can increase image detection precision.

- `--match-step` <number>
    - Match step when finding image. Step size determines how many rows are
      skipped during image detection. For example, value 3 will skip two rows
      when finding the image. Higher value means faster detection, but lowers
      accuracy. Useful for very high-res displays. Value 2 is default and offers
      good balance between speed and accuracy on lower-res displays.

- `--pause-on-fail`
    - Pause execution if current instruction fails, instead of exiting.

## Recording mode

Recording mode records the user activity (clicking and waiting)
and generates a macro with recorded activity.

- `--output`, `-o` <file>
    - Output file. If not specified, standard output is used.

## Check mode

Check mode checks provided input file and reports any issues found.

- `--file`, `-f` <file>
    - The file to be checked.
- `--full`
    - Perform full check - additionally check labels and image paths.

## Show coords mode

Show coords of a mouse click.

This mode has no additional parameters.