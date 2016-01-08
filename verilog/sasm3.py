# - Simplez assembler
# - Grammar definition
# -
# --- A program is a list of lines with the END keyword in the end (finished by EOL)
# --- Notice that after the END there could be more instructions, but they will be ignored
# <program> ::= <lines> "END" EOL
#
# --- There could be more than one lines. Each line should be end by EOL
# <lines> ::= <line> EOL | <lines>
#
# -- Each line can be a comment, a line of code followed by a commnet
# -- or just a simple line of code
# <line> ::= COMMENT | <lineofcode> COMMENT | <lineofcode>
#
# -- Lines of code can be either a directive or line with a simplez instructions
# <lineofcode> ::= <directive> | <lineinstruction>
#
# -- All the instruction can have a label in the beginning of the line (optionally)
# <lineinstruction> ::= <instruction> | LABEL <instruction>
#
# -- There are 9 different simplez-F instructions
# <instruction> ::= <instLD>  | <insST>   | <instADD>  | <instBR> | <instBZ> |
# ----------------- <instCLR> | <instDEC> | <instHALT> | <instWAIT>
#

# - There are 4 different directives
# <directive> ::= <dirORG> | <dirEQU> | <dirRES> | <dirDATA>
#
# - ORG directive do not have any label in the left. The argument can be a number or a label
# - label (defined by the EQU directive)
# <dirORG> ::= ORG NUMBER | ORG LABEL
#
# -- EQU Directive
# <dirEQU> ::= LABEL EQU NUMBER
#
# -- DATA directive.  Label is optional
# <dirDATA> ::= LABEL DATA <datacollection> |  DATA <datacollection>
#
# -- Collection of data,separated by ,
# <datacollection> ::= <data> (,<data>)*
#
# -- Type of data accepted as "DATA"
# <data> ::= STRING | NUMBER
#
# -- RES directive. Label is optional
# <dirRES> ::= LABEL RES NUMBER | RES NUMBER
#

# -- Instruction LD
# <instLD> ::= LD <addr>
#
# -- The address can be giben numerically (eg. /501), or by label (eg. /ini)
# <addr> ::= ADDRNUM | ADDRLABEL
#
# -- Instruction ST
# <instST> ::= ST <addr>
#
# -- Instruction ADD
# <instADD> ::= ADD <addr>
#
# -- Instruction BR
# <instBR> ::= BR <addr>
#
# -- Instruction BZ
# <instrBZ> ::= BZ <addr>
#
# -- Instruction CLR
# <instrCLR> ::= CLR
#
# -- Instruction DEC
# <instrDEC> ::= DEC
#
# -- Istruction HALT
# <instrHAL> ::= HALT
#
# -- Instruction WAIT
# <instWAIT> ::= WAIT

# - Tokens:
#
# - EOL, EOF, COMMENT, LABEL, ORG, NUMBER, STRING, ADDRNUM, ADDRLABEL
# - LD, ST, ADD, BR, BZ, CLR, DEC, HALT, WAIT

# - COMMENT: ;(any ascii char)*
# - LABEL: (any ascii char)*  That is NOT a reserved word
# - NUMBER: Decimal or hexadecimal number:  [0-9]* | H'[0-9,a-f,A-F]*
# - STRING: "(any ascii char)"
# - ADDRNUM: /NUMBER
# - ADDRLABEL: /LABEL
