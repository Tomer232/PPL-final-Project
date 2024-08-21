import re


class Lexer:
    def __init__(self, code):
        self.code = code
        self.line_num = 1
        self.line_start = 0
        self.tokens = []

    token_spec = [
        ('DEFUN', r'\bDefun\b'),  # Function definition keyword
        ('NAME', r'\bname\b'),  # Function name reserved word
        ('ARGUMENTS', r'\barguments\b'),  # Function arguments reserved word
        ('LAMBD', r'\bLambd\b'),  # Lambda keyword
        ('IF', r'\bif\b'),  # If keyword
        ('ELSE', r'\belse\b'),  # Else keyword
        ('INTEGER', r'-?\d+'),  # Integer (including negative integers)
        ('BOOLEAN', r'\bTrue\b|\bFalse\b'),  # Boolean
        ('LETTER', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),  # Identifiers
        ('BASIC_OP', r'[-+*/%]'),  # Arithmetic Operators
        ('BOOL_OP', r'&&|\|\|'),  # Boolean Operators
        ('COMP_OP', r'==|!=|>=|<=|>|<'),  # Comparison Operators
        ('NOT', r'!'),                # Not Operators
        ('LPAREN', r'\('),            # Left parenthesis
        ('RPAREN', r'\)'),            # Right parenthesis
        ('LBRACE', r'\{'),            # Left brace
        ('RBRACE', r'\}'),            # Right brace
        ('COMMA', r','),              # Comma
        ('COLON', r':'),              # Colon
        ('DOT', r'\.'),               # Dot
        ('NEWLINE', r'\n'),           # Line endings
        ('JUMP', r'[ \t]+'),          # Skip over spaces and tabs
        ('COMMENT', r'#.*'),         # Single line comment
        ('INVALID', r'.'),           # Any other character
    ]

    # The master regular expression
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_spec)

    def tokenize(self):
        for movj in re.finditer(self.tok_regex, self.code):
            kind = movj.lastgroup
            value = movj.group(kind)
            column = movj.start() - self.line_start
            if kind == 'INTEGER':
                value = int(value)
            elif kind == 'NEWLINE':
                self.line_start = movj.end()
                self.line_num += 1
                continue
            elif kind == 'BOOLEAN':
                value = True if value == 'True' else False
            elif kind == 'JUMP' or kind == 'COMMENT':
                continue
            elif kind == 'INVALID':
                raise RuntimeError(f'{value!r} unexpected on line {self.line_num}')
            self.tokens.append((kind, value, self.line_num, column))
        self.tokens.append(('EOF', 'EOF', self.line_num, column))
        return self.tokens
