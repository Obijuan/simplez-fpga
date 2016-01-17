#!/usr/bin/python3

import ply.lex as lex

tokens = (
   'COMMENT',
   'ADDR',      # -- Value: addr (in hexa)
   'DATA',      # -- Value: Data (in hexa)
)

t_ignore = ' \t\r\f\v'


# - Comments are ignored
def t_COMMENT(t):
    r'//[^\n]*'
    pass


def t_DATA(t):
    r'[0-9a-fA-F]+'
    t.value = int(t.value, 16)
    return t


def t_ADDR(t):
    r'@[0-9a-fA-F]+'
    t.value = int(t.value[1:], 16)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

data = '''
//-- Hola
@40  //-- Comienzo
gg
10 20   //-- Una inst
30   //-- Otra...
caca
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok.type, tok.value, tok.lineno, tok.lexpos)
    # print(tok)
