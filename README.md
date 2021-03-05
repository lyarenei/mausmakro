# Mausmakro

Mausmakro is a mouse macro player for automating various time-consuming and
repeating tasks on your computer.

## Why

Over time, I tried a few of these "mouse macro players" with a varying set of
features. Some of them offered quite advanced features, but that always came
with a need to buy a licence to unlock all features. I don't have a problem with
that as a whole, however, these licences were too expensive or there wasn't a "
cheap enough" tier to unlock the features I needed. So I decided to write my
own, completely free.

### Features

- Well, of course, there's a simple click/double-click to a given set of
  coordinates
- Image detection (find a picture on the screen)
    - This includes clicking on the image if it's found
- A simple recorder of the user's actions (only clicking and waiting is
  recorded)
    - This is useful for quick and dirty macro creation
- Mouse coords display mode, so you know where the pointer clicks
- Infinite macro replays (often required a licence in other software)

The macros are written in their own simple language. As the language kind of
resembles a programming language, it also includes some extra bits which allows
you to write a more complex macros:

- Branching support (if-else)
- Jumping - and by extension simple loops
- Procedure calling (code re-usability)

### Supported platforms

Mausmakro is written in python and all dependencies should support all three
major platforms:
Linux (excluding Wayland), Windows, macOS. Most of the time I use macOS and
sometimes Windows, so I verified it works there, but unfortunately, I don't have
a linux desktop, so I can't verify the functionality there.

### How to use

Mausmakro is fairly straightforward to use, it takes a file with macros as an
input and then does its thing.  
At this moment, Mausmakro can be installed from test pip
instance: `pip install -i https://test.pypi.org/simple/ mausmakro`
Alternatively, you can clone this repository and install it
locally: `pip install .`

If you are on macOS, you also need to give following permissions to your
terminal:

- Screen recording
- Input monitoring
- Accessibility

There are four modes available, check, record, show-coords and interpret. An
example for interpreting a macro can
be `python -m mausmakro interpret -f foobar.mkr -m save_me`
Which will interpret macro named `save_me` in file `foobar.mkr` in an infinite
loop. To see other options, use `--help` parameter or check
the [manual](doc/manual.md).

The mausmakro execution can be paused by specific instruction or manually with
left `Ctrl` key. To resume execution, press the left `Ctrl` key again.
The `Ctrl` key is detected independently on which window is active, allowing
pausing quickly if necessary. This functionality is only available in
the `interpret` mode.

To exit, in any mode, use the standard `Ctrl+C` keyboard shortcut.

### Writing macros

Writing macros is pretty easy, albeit a bit time-consuming, especially if you
are writing a more complex one. If you are more of a technical person, who knows
what EBNF is, you can read the EBNF [here](doc/ebnf.md). Otherwise, there are a
few rules:

- The input file must contain at least one macro
- Every code body (macro, procedure, if/else) begins with `{` and ends with `}`
- A Macro/procedure always requires a unique label
- Only one command per line is allowed
- Macros/procedures cannot be nested
- IF statement may have an ELSE branch

All available commands are described [here](doc/commands.md). You can also look
for an example [here](examples/simple.mkr).

## Development

In order to write a new functionality, you need to set up a development
environment. The process is very easy and mausmakro is just your another python
project.

1) Make sure you have at least python 3.6 installed
2) Clone the repo
3) Create a virtual environment: `python3 -m venv .env`
4) Activate new environment: `source .env/bin/activate`
5) Install dependencies: `pip install -r requirements.txt`

If you get a compile errors, an installation of a `wheel` package might help.
Simply run `pip install wheel` inside the virtual environment, then try again.  
