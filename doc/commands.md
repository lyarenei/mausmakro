# Available commands

These commands are available to user to write macros

- CALL `<label>`
    - call (execute) a procedure/macro
    - allows returning back, unlike JUMP command
    - example: `CALL foo`


- CLICK `<x,y>`
    - click on specified coordinates
    - x is width, y is height
    - example: `CLICK 42,42`


- CLICK ON `<image>` WITHIN `<number><unit>`
    - click on specified image
    - this image must be found within number of units time
    - unit can be s,m,h (second, minute, hour)
    - **cannot** be used in `IF` command
    - example: `CLICK on foobar.png WITHIN 5s`


- EXIT
    - stop the macro execution


- FIND `<image>` WITHIN `<number><unit>`
    - find the image, then proceed
    - same rules apply as in `CLICK ON` command
    - **can** be used in `IF` command
    - example: `FIND foobar.png WITHIN 5s`


- IF <conditional>
    - conditional execution of a set of commands
        - if image is found, do this
        - if image is not found, do that
    - example: `IF FIND foobar.png WITHIN 5s { }`


- IF NOT <conditional>
    - an inverted version of the IF statement
        - if image is not found, do this
        - if image is found, do that
    - example: `IF NOT FIND foobar.png WITHIN 5s { }`


- JUMP TO <label>
    - jump to a label in the macro file
    - only one-way, use CALL if you need to be able to return
    - example: `JUMP TO foobar`


- LABEL <label>
    - name a section of code from its position until the end of macro
    - example: `LABEL foobar`


- PAUSE
    - pause a macro execution indefinitely
    - can be resumed by the user
    - for an automated execution resume, use WAIT command


- PCLICK
    - The precise version of the `CLICK ON` command
    - Internally uses the best parameters for detection, in exchange for speed
    - Useful when getting false positives on that particular image


- PFIND
    - The precise version of the `FIND` command
    - Internally uses the best parameters for detection, in exchange for speed
    - Useful when getting false positives on that particular image


- RETURN
    - return to position before calling
    - cannot be used if there's nowhere to go back (cannot be used without prior
      CALL)


- WAIT <number><unit>
    - wait a specified amount of time
    - unit can be s,m,h (second, minute, hour)
    - example: `WAIT 10s`

For the sake of a documentation completeness, these commands are used internally
and cannot be used in the macros by the user.

- END
    - marks the end of a main macro execution
