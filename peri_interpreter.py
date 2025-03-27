#Building my First Programming Language


#Writing the Lexical Analysis Phase
# peri_interpreter.py

import re

# Token types
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
    ('WHILE', r'while'),
    ('PRINT', r'print'),
    ('STRING', r'"[^"]*"'),
    ('SEMICOLON', r';'),  # Add semicolon support
    ('SKIP', r'[ \t\n]'),  # Skip whitespace
    ('MISMATCH', r'.'),    # Any other character
]

# Lexer
def lex(code):
    tokens = []
    while code:
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(code)
            if match:
                value = match.group(0)
                if token_type != 'SKIP':
                    tokens.append((token_type, value))
                code = code[match.end():]
                break
        else:
            # Print the problematic character and remaining code
            print(f"Remaining code: {code}")
            print(f"Unexpected character: {code[0]}")
            raise SyntaxError(f"Unexpected character: {code[0]}")
    return tokens

#Write the Parser : The parser converts tokens into an Abstract Syntax Tree (AST).
# peri_interpreter.py

class ASTNode:
    pass

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class Assign(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Print(ASTNode):
    def __init__(self, value):
        self.value = value

def parse(tokens):
    if tokens[0][0] == 'NUMBER':
        return Number(int(tokens.pop(0)[1]))
    elif tokens[0][0] == 'IDENTIFIER':
        return tokens.pop(0)[1]
    elif tokens[0][0] == 'STRING':
        return tokens.pop(0)[1][1:-1]  # Remove quotes from string
    else:
        raise SyntaxError("Invalid expression")

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
            raise SyntaxError(f"Unexpected token: {value}")
    return ast


# Writing a Interpreter 
# peri_interpreter.py

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
    elif isinstance(node, str):  # Handle string literals
        return node
    else:
        raise RuntimeError(f"Unknown node type: {type(node)}")

    def interpret(self, ast):
        for node in ast:
            self.visit(node)

# peri_interpreter.py

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python peri_interpreter.py <file.peri>")
        return

    with open(sys.argv[1], 'r') as file:
        code = file.read()

    
    tokens = lex(code)
    ast = parse(tokens)
    interpreter = Interpreter()
    interpreter.interpret(ast)
    

if __name__ == '__main__':
    main()


