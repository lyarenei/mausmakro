# EBNF

This is an EBNF used by the parser to parse the macro files. If you can read it,
great. If you can't, don't worry, ignore it.

Note: Mausmakro uses [Lark](https://lark-parser.readthedocs.io/en/latest/) 
for the input file parsing, so the EBNF here is not in its pure form, but some Lark extensions
are used as well.

```text
%import common.DIGIT
%import common.INT
%import common.LETTER
%import common.NEWLINE
%import common.WS
%ignore /#[^\n]*/
%ignore INDENT
%ignore NEWLINE
%ignore WS
FILENAME                       : /[\w\-_\/]+/
EXTENSION                      : "jpeg" | "jpg" | "png"
INDENT                         : /\t| {4}| {2}/
NAME            : (LETTER | "_" | "-" | DIGIT)+
FILE            : FILENAME "." EXTENSION
COORDS          : INT WS* "," WS* INT
TIME            : INT WS* ("s" | "m" | "h")
call            : "CALL" NAME
click           : "CLICK" (COORDS | "ON" FILE "WITHIN" TIME)
double_click    : "DOUBLE_CLICK" COORDS
find            : "FIND" FILE "WITHIN" TIME
jump            : "JUMP" "TO" NAME
label           : "LABEL" NAME
pause           : "PAUSE"
pclick          : "PCLICK" (COORDS | "ON" FILE "WITHIN" TIME)
pfind           : "PFIND" FILE "WITHIN" TIME
return          : "RETURN"
wait            : "WAIT" TIME
instruction     : call
                | click
                | double_click
                | find
                | jump
                | label
                | pause
                | pclick
                | pfind
                | return
                | wait
body            : "{" (instruction | conditional | neg_conditional)+ "}"
conditional     : "IF" (find | pfind) body ("ELSE" body)?
procedure       : "PROC" NAME body
neg_conditional : "IF NOT" find body ("ELSE" body)?
macro           : "MACRO" NAME body 

start           : (macro | procedure)+
```