import re

# --- Token types
INTEGER, PLUS, MINUS, MULT, DIV, EOF, UNKNOWN = ('INTEGER', 'PLUS', 'MINUS', 'MULT', 'DIV',
                                                 'EOF', 'UNKNOWN')

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


class Interpreter(object):
    """Main interpreter"""

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):

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
            token = Token(MULT, current_char)
            self.pos += 1
            return token

        if current_char == '/':
            token = Token(DIV, current_char)
            self.pos += 1
            return token

        # - Token desconocido
        token = Token(UNKNOWN, None)
        self.pos += 1
        return token

    def assert_type(self, type):
        """Make sure the current token is of the given type"""

        if self.current_token.type == type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def test(self):
        for i in range(10):
            print(self.get_next_token())

        return ""

    def expr(self):
        """Evaluate the text given"""

        # ---- Expresions to parser:
        #   INTEGER PLUS INTEGER
        #   INTEGER MINUS INTEGER
        #   INTEGER MULT INTEGER
        #   INTEGER DIV INTEGER

        # Get the current token
        self.current_token = self.get_next_token()

        # - Left operand
        left = self.current_token
        self.assert_type(INTEGER)

        # - Parcial result
        result = left.value

        while self.current_token.type != EOF:

            # -- Operator +
            op = self.current_token
            if op.type == PLUS:
                self.assert_type(PLUS)
            elif op.type == MINUS:
                self.assert_type(MINUS)
            elif op.type == MULT:
                self.assert_type(MULT)
            else:
                self.assert_type(DIV)

            # -- Right operand
            right = self.current_token
            self.assert_type(INTEGER)

            if op.type == PLUS:
                result += right.value
            elif op.type == MINUS:
                result -= right.value
            elif op.type == MULT:
                result *= right.value
            else:
                result /= right.value

        return int(result)


if __name__ == '__main__':
    while True:
        try:
            text = input('test> ')
        except EOFError:
            break
        if not text:
            continue
        interp = Interpreter(text)
        result = interp.expr()
        # result = interp.test()
        print(result)
