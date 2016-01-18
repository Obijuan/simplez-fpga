#!/usr/bin/python3

import ply.lex as lex


class Lexer(object):

    tokens = (
       'COMMENT',
       'ADDR',      # -- Value: addr (in hexa)
       'DATA',      # -- Value: Data (in hexa)
       'EOF'
    )

    t_ignore = ' \t\r\f\v'

    def __init__(self, data):
        """Create the lexer and give the data"""
        self.lexer = lex.lex(module=self)
        self.lexer.input(data)

        # -- Read the first token
        self.current_token = self.lexer.token()

        # -- Address pointer. It contains the current address
        self.addr = 0

    # - Comments are ignored
    def t_COMMENT(self, t):
        r'//[^\n]*'
        pass

    def t_DATA(self, t):
        r'[0-9a-fA-F]+'
        t.value = int(t.value, 16)
        return t

    def t_ADDR(self, t):
        r'@[0-9a-fA-F]+'
        t.value = int(t.value[1:], 16)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_eof(self, t):
        t.type = 'EOF'
        t.value = ''
        return t

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def token(self):
        """Read the next token"""
        self.current_token = self.lexer.token()

    def get_block(self):
        """Return the next memory block. It returns:
        (initial address, memory block)"""

        # -- Initial address = current address
        init_addr = self.addr

        # -- Current memory block
        bmem = []

        if self.current_token.type == "EOF":
            return None, None

        if self.current_token.type == "ADDR":

            # -- Updte the initial address
            init_addr = self.current_token.value

            # -- Read the next token
            self.token()

        while self.current_token.type == "DATA":
            # -- Add the data to the memory block
            bmem.append(self.current_token.value)

            self.token()

        return init_addr, bmem

# -- Main program
if __name__ == '__main__':

    data = '''
    //-- Hola
    @10
    20
    @40  //-- Comienzo
    10 20   //-- Una inst
    30   //-- Otra...
    caca
    @50
    '''

    data2 = '''
    @10
    '''
    data3 = ''' '''

    # Create the lexer with some data
    l = Lexer(data)

    # -- Read the first block
    init_addr, bmem = l.get_block()
    i = 1

    # -- Read every block and print its information
    while init_addr:
        print("Block {}".format(i))
        print("  Addr: {:03X}".format(init_addr))
        print("  Size: {}".format(len(bmem)))
        print("  Mem: {}".format(bmem))
        print()

        init_addr, bmem = l.get_block()
        i += 1
