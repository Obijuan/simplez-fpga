import re

# --- Token types
INTEGER, PLUS, MINUS, MUL, DIV, LPAR, RPAR, EOF, UNKNOWN = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAR', 'RPAR', 'EOF', 'UNKNOWN'
)

# -------- Regular expresions
# -- White spaces
REGEX_WSPACE = r"[\s]+"

# -- Decimal number
REGEX_DEC = r"[0-9]+"

# -- Hexadecimal number
REGEX_HEX = r"0x[0-9a-fA-F]+"


class Token(object):
    """Token generator"""

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "TOKEN({}, {})".format(self.type, self.value)


class Lexer(object):
    """Lexical analyzer"""

    def __init__(self, text):
        self.text = text
        self.pos = 0

    def reset(self):
        self.pos = 0

    def get_token(self):
        """Get the next token from tex"""

        # - Remove the white spaces, if any
        scan = re.match(REGEX_WSPACE, self.text[self.pos:])
        if scan:
            self.pos += len(scan.group())

        # -- Check if it is an hexadecimal number
        scan = re.match(REGEX_HEX, self.text[self.pos:])
        if scan:
            self.pos += len(scan.group())
            token = Token(INTEGER, int(scan.group(), 16))
            return token

        # -- Check if it is a decimal number
        scan = re.match(REGEX_DEC, self.text[self.pos:])
        if scan:
            self.pos += len(scan.group())
            token = Token(INTEGER, int(scan.group()))
            return token

        # --Get the current char
        try:
            current_char = self.text[self.pos]
        except IndexError:
            return Token(EOF, None)

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token

        if current_char == '*':
            token = Token(MUL, current_char)
            self.pos += 1
            return token

        if current_char == '/':
            token = Token(DIV, current_char)
            self.pos += 1
            return token

        if current_char == '(':
            token = Token(LPAR, current_char)
            self.pos += 1
            return token

        if current_char == ')':
            token = Token(RPAR, current_char)
            self.pos += 1
            return token

        # - Token desconocido
        token = Token(UNKNOWN, None)
        self.pos += 1
        return token

    def test(self):
        """Test the lexer"""
        while True:
            token = self.get_token()
            print(token)
            if token.type == EOF:
                return


class Interpreter(object):
    """Main interpreter"""

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_token()

    def error(self):
        raise Exception('Error parsing input')

    def assert_type(self, type):
        """Make sure the current token is of the given type"""

        if self.current_token.type == type:
            self.current_token = self.lexer.get_token()
        else:
            self.error()

    def factor(self):
        """factor : INTEGER | pexpr """
        if self.current_token.type == INTEGER:
            value = self.current_token.value
            self.assert_type(INTEGER)
            return value
        else:
            return self.pexpr()

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""

        result = self.factor()
        while self.current_token.type in (MUL, DIV):

            if self.current_token.type == MUL:
                self.assert_type(MUL)
                result = result * self.factor()

            elif self.current_token.type == DIV:
                self.assert_type(DIV)
                result = int(result / self.factor())

        return result

    def pexpr(self):
        """pexpr: LPAR expr RPAR"""
        self.assert_type(LPAR)
        result = self.expr()
        self.assert_type(RPAR)
        return result

    def expr(self):
        """expr : term ((PLUS | MINUS) term)*
           term : factor ()(MUL | DIV) factor)*
           factor: INTEGER
        """
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):

            if self.current_token.type == PLUS:
                self.assert_type(PLUS)
                result = result + self.term()

            elif self.current_token.type == MINUS:
                self.assert_type(MINUS)
                result = result - self.term()

        return result


if __name__ == '__main__':
    while True:
        try:
            text = input('test> ')
        except EOFError:
            break
        if not text:
            continue

        # - Lexical analyzer
        lexer = Lexer(text)

        # - Test
        lexer.test()
        lexer.reset()

        interp = Interpreter(lexer)
        print (interp.expr())
