import re

# ====================== LEXER ======================
TOKENS = [
    ('NUMBER', r'\d+'),
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),
    ('ASSIGN', r'='),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('IF', r'if'),
    ('ELSE', r'else'),
    ('WHILE', r'while'),
    ('PRINT', r'print'),
    ('STRING', r'"[^"]*"'),
    ('SEMICOLON', r';'),
    ('SKIP', r'[ \t\n]'),  # Whitespace
    ('MISMATCH', r'.'),    # Unrecognized characters
]

def lex(code):
    tokens = []
    pos = 0
    while pos < len(code):
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                value = match.group(0)
                if token_type != 'SKIP':
                    tokens.append((token_type, value))
                pos = match.end()
                break
        else:
            raise SyntaxError(f"Unexpected character: '{code[pos]}' at position {pos}")
    return tokens

# ====================== PARSER ======================
class ASTNode:
    pass

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Assign(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Print(ASTNode):
    def __init__(self, value):
        self.value = value

def parse(tokens):
    ast = []
    while tokens:
        token_type, value = tokens[0]
        
        if token_type == 'PRINT':
            tokens.pop(0)
            ast.append(Print(parse_expression(tokens)))
        elif token_type == 'IDENTIFIER' and len(tokens) > 1 and tokens[1][0] == 'ASSIGN':
            name = tokens.pop(0)[1]
            tokens.pop(0)  # Remove '='
            ast.append(Assign(name, parse_expression(tokens)))
        else:
            raise SyntaxError(f"Unexpected token: '{value}'")

    return ast

def parse_expression(tokens):
    if not tokens:
        raise SyntaxError("Unexpected end of input")

    token_type, value = tokens[0]
    
    if token_type == 'NUMBER':
        tokens.pop(0)
        return Number(int(value))
    elif token_type == 'IDENTIFIER':
        tokens.pop(0)
        return value
    elif token_type == 'STRING':
        tokens.pop(0)
        return value[1:-1]  # Remove quotes
    else:
        raise SyntaxError(f"Invalid expression: '{value}'")

# ====================== INTERPRETER ======================
class Interpreter:
    def __init__(self):
        self.variables = {}

    def visit(self, node):
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            if node.op == '+':
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                return left / right
        elif isinstance(node, Assign):
            self.variables[node.name] = self.visit(node.value)
        elif isinstance(node, Print):
            value = self.visit(node.value)
            print(value)
        elif isinstance(node, str):
            return self.variables.get(node, f"<undefined variable '{node}'>")
        else:
            raise RuntimeError(f"Unknown node type: {type(node)}")

    def interpret(self, ast):
        for node in ast:
            self.visit(node)

# ====================== MAIN ======================
def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python peri_interpreter.py <file.peri>")
        return

    try:
        with open(sys.argv[1], 'r') as file:
            code = file.read()

        tokens = lex(code)
        ast = parse(tokens)
        interpreter = Interpreter()
        interpreter.interpret(ast)

    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found.")
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    except RuntimeError as e:
        print(f"Runtime Error: {e}")

if __name__ == '__main__':
    main()