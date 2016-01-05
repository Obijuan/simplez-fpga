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


class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def eval(self):
        if self.op.type == MUL:
            return self.left.eval() * self.right.eval()
        elif self.op.type == DIV:
            return int(self.left.eval() / self.right.eval())
        elif self.op.type == PLUS:
            return self.left.eval() + self.right.eval()
        elif self.op.type == MINUS:
            return self.left.eval() - self.right.eval()


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def eval(self):
        return self.value


class Parser(object):
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

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""

        node = self.factor()
        while self.current_token.type in (MUL, DIV):

            token = self.current_token
            self.assert_type(token.type)
            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        """factor : INTEGER | LPAR expr RPAR """
        if self.current_token.type == INTEGER:
            token = self.current_token
            self.assert_type(INTEGER)
            return Num(token)
        else:
            self.assert_type(LPAR)
            node = self.expr()
            self.assert_type(RPAR)
            return node

    def expr(self):
        """expr : term ((PLUS | MINUS) term)*
        #  term : factor ()(MUL | DIV) factor)*
        #  factor: INTEGER
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            self.assert_type(token.type)
            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):
        return self.expr()


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return int(self.visit(node.left) / self.visit(node.right))

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        # - Create the AST
        ast = self.parser.parse()

        # - Evaluate the ast
        return self.visit(ast)


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
        # lexer.test()
        # lexer.reset()

        # - Parser
        parser = Parser(lexer)

        # - Test
        # ast = parser.parse()
        # print(ast.eval())

        # - Interpreter
        interp = Interpreter(parser)
        print (interp.interpret())
