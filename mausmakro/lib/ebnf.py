from mausmakro.lib.enums import ArgType, Opcode

ebnf = r"""
%import common.DIGIT
%import common.INT
%import common.LETTER
%import common.NEWLINE
%import common.WS

%ignore /#[^\n]*/
%ignore NEWLINE
%ignore WS

FILENAME                       : /[\w\-_\/]+/
EXTENSION                      : "jpeg" | "jpg" | "png"
""" + f"""
{ArgType.NAME.name}            : (LETTER | "_" | "-" | DIGIT)+
{ArgType.FILE.name}            : FILENAME "." EXTENSION
{ArgType.COORDS.name}          : INT WS* "," WS* INT
{ArgType.TIME.name}            : INT WS* ("s" | "m" | "h")

{Opcode.CALL.value}            : "{Opcode.CALL.name}" {ArgType.NAME.name}
{Opcode.CLICK.value}           : "{Opcode.CLICK.name}" ({ArgType.COORDS.name} | "ON" {ArgType.FILE.name} "WITHIN" {ArgType.TIME.name})
{Opcode.DOUBLE_CLICK.value}    : "{Opcode.DOUBLE_CLICK.name}" {ArgType.COORDS.name}
{Opcode.FIND.value}            : "{Opcode.FIND.name}" {ArgType.FILE.name} "WITHIN" {ArgType.TIME.name}
{Opcode.JUMP.value}            : "{Opcode.JUMP.name}" "TO" {ArgType.NAME.name}
{Opcode.LABEL.value}           : "{Opcode.LABEL.name}" {ArgType.NAME.name}
{Opcode.PAUSE.value}           : "{Opcode.PAUSE.name}"
{Opcode.PCLICK.value}          : "{Opcode.PCLICK.name}" ({ArgType.COORDS.name} | "ON" {ArgType.FILE.name} "WITHIN" {ArgType.TIME.name})
{Opcode.PFIND.value}           : "{Opcode.PFIND.name}" {ArgType.FILE.name} "WITHIN" {ArgType.TIME.name}
{Opcode.RETURN.value}          : "{Opcode.RETURN.name}"
{Opcode.WAIT.value}            : "{Opcode.WAIT.name}" {ArgType.TIME.name}

instruction     : {Opcode.CALL.value}
                | {Opcode.CLICK.value}
                | {Opcode.DOUBLE_CLICK.value}
                | {Opcode.FIND.value}
                | {Opcode.JUMP.value}
                | {Opcode.LABEL.value}
                | {Opcode.PAUSE.value}
                | {Opcode.PCLICK.value}
                | {Opcode.PFIND.value}
                | {Opcode.RETURN.value}
                | {Opcode.WAIT.value}
""" + r"""
body            : "{" (instruction | conditional | neg_conditional)+ "}"
""" + f"""
conditional     : "IF" ({Opcode.FIND.value} | {Opcode.PFIND.value}) body ("ELSE" body)?
procedure       : "PROC" {ArgType.NAME.name} body
neg_conditional : "IF NOT" {Opcode.FIND.value} body ("ELSE" body)?
macro           : "MACRO" {ArgType.NAME.name} body 
start           : (macro | procedure)+
"""
