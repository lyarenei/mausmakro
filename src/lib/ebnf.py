from lib.enums import ArgType, Opcode

ebnf = r"""
%import common.INT
%import common.LCASE_LETTER
%import common.NEWLINE
%import common.WS

%ignore /#[^\n]*/
%ignore INDENT
%ignore NEWLINE
%ignore WS

FILENAME                       : /[\w\-_\/]+/
EXTENSION                      : "jpeg" | "jpg" | "png"
INDENT                         : /\t| {4}| {2}/
""" + f"""
{ArgType.NAME.name}            : (LCASE_LETTER | "_" | "-")+
{ArgType.FILE.name}            : FILENAME "." EXTENSION
{ArgType.COORDS.name}          : INT "," INT
{ArgType.TIME.name}            : INT "s"|"m"|"h"

{Opcode.CALL.value}            : "{Opcode.CALL.name}" {ArgType.NAME.name}
{Opcode.CLICK.value}           : "{Opcode.CLICK.name}" ({ArgType.COORDS.name} | "ON" {ArgType.FILE.name} "WITHIN" {ArgType.TIME.name})
{Opcode.DOUBLE_CLICK.value}    : "{Opcode.DOUBLE_CLICK.name}" {ArgType.COORDS.name}
{Opcode.FIND.value}            : "{Opcode.FIND.name}" {ArgType.FILE.name} "WITHIN" {ArgType.TIME.name}
{Opcode.JUMP.value}            : "{Opcode.JUMP.name}" "TO" {ArgType.NAME.name}
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
