from ast_node import FuncDef, LambdaExpr, FuncApp, Identifier, IntLit, BoolLit, UnaryOp, BinOp, IfStmt


class BNFLoader:
    def __init__(self, bnf_file_path):
        self.rules = self.grammar(bnf_file_path)

    def grammar(self, file_path_way):
        rules = {}
        with open(file_path_way, 'r') as f:
            content = f.read()
            lines = content.splitlines()
            current_non_terminal = None
            for line in lines:
                if line.strip() == "":
                    continue
                if "::=" in line:
                    parts = line.split("::=")
                    current_non_terminal = parts[0].strip()
                    rules[current_non_terminal] = [p.strip() for p in parts[1].split("|")]
                else:
                    rules[current_non_terminal].extend([p.strip() for p in line.split("|")])
        return rules


class Parser:
    def __init__(self, toks, bnf_path=None, debug=False):
        self.tokens = toks
        self.position = 0
        self.current_token = self.tokens[self.position] if toks else None
        self.debug = debug
        self.rules = BNFLoader(bnf_path).rules if bnf_path else None

    '''def log(self, message):
        if self.debug:
            print(message)'''

    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = ('EOF', 'EOF', -1, -1)

    def error(self, message):
        line = self.current_token[2]
        col = self.current_token[3]
        raise SyntaxError(
            f"Syntax Error at line {line}, column {col}: {message}. Current token: {self.current_token[0]}")

    def parse(self):
        try:
            result = self.program()
            return result
        except Exception as e:
            raise RuntimeError(f"Parsing failed: {str(e)}")

    def expect(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            self.advance()
        else:
            self.error(f"Expected token {token_type} but got {self.current_token[0]}")

    def parse_statement(self):
        if self.current_token[0] == 'DEFUN':
            return self.parse_function_def()
        elif self.current_token[0] == 'IF':
            return self.parse_if_statement()
        elif self.current_token[0] == 'LPAREN' and self.tokens[self.position + 1][0] == 'LAMBD':
            return self.parse_lambda_expr()
        else:
            return self.parse_expression()

    def program(self):
        statements = []
        while self.current_token[0] != 'EOF':
            statements.append(self.parse_statement())
        return statements

    def parse_function_def(self):
        try:
            self.expect('DEFUN')
            self.expect('LBRACE')
            self.expect('NAME')
            self.expect('COLON')
            func_name = self.current_token[1]
            self.expect('LETTER')
            self.expect('COMMA')
            self.expect('ARGUMENTS')
            self.expect('COLON')
            params = self.parse_params()
            self.expect('RBRACE')
            if self.current_token[0] == 'IF':
                body = self.parse_if_statement()
            else:
                body = self.parse_expression()
            return FuncDef(func_name=func_name, parameters=params, func_body=body)
        except SyntaxError as e:
            self.error(f"Error parsing function definition: {e}")

    def parse_if_statement(self):
        try:
            self.expect('IF')
            condition = self.parse_expression()
            self.expect('LBRACE')
            consequence = self.parse_expression()
            self.expect('RBRACE')
            alternative = None
            if self.current_token[0] == 'ELSE':
                self.expect('ELSE')
                self.expect('LBRACE')
                alternative = self.parse_expression()
                self.expect('RBRACE')
            return IfStmt(condition, consequence, alternative)
        except SyntaxError as e:
            self.error(f"Error parsing if statement: {e}")

    def parse_lambda_expr(self):
        self.expect('LPAREN')
        self.expect('LAMBD')
        if self.current_token[0] == 'LETTER':
            params = self.current_token[1]
            self.expect('LETTER')
            self.expect('DOT')
        body = self.parse_expression()
        self.expect('RPAREN')
        lambda_expr = LambdaExpr(parameters=params, expr_body=body)
        if self.current_token[0] == 'LPAREN':
            return self.parse_lambda_call(lambda_expr)
        return lambda_expr

    def parse_function_call(self, func):
        func = self.current_token[1]
        self.expect('LETTER')
        self.expect('LPAREN')
        args = self.parse_args()
        self.expect('RPAREN')
        return FuncApp(function=func, arguments=args)

    def parse_lambda_call(self, func):
        self.expect('LPAREN')
        args = self.parse_args()
        self.expect('RPAREN')
        return FuncApp(function=func, arguments=args)

    def parse_args(self):
        args = []
        while self.current_token[0] != 'RPAREN':
            args.append(self.parse_expression())
            if self.current_token[0] == 'COMMA':
                self.expect('COMMA')
            elif self.current_token[0] == 'RPAREN':
                break
            else:
                self.error(f"Unexpected token in argument list: {self.current_token}")
        return args

    def parse_params(self):
        params = []
        self.expect('LPAREN')
        while self.current_token[0] == 'LETTER' and self.tokens[self.position + 1][0] == 'COMMA':
            params.append(self.current_token[1])
            self.expect('LETTER')
            self.expect('COMMA')
        self.expect('RPAREN')
        return params

    def parse_expression(self):

        def parse_term():
            if self.current_token[0] == 'NOT':
                op = self.current_token[1]
                self.expect('NOT')
                expr = self.parse_expression()
                unary_op = UnaryOp(op, expr)
                return unary_op

            if self.current_token[0] == 'LPAREN' and self.position + 1 < len(self.tokens) and self.tokens[self.position + 1][0] == 'LAMBD':
                return self.parse_lambda_expr()

            if self.current_token[0] == 'LETTER' and self.position + 1 < len(self.tokens) and self.tokens[self.position + 1][0] == 'LPAREN':
                return self.parse_function_call(self.current_token[1])

            if self.current_token[0] == 'INTEGER':
                number = IntLit(self.current_token[1])
                self.expect('INTEGER')
                return number

            if self.current_token[0] == 'LETTER':
                identifier = Identifier(self.current_token[1])
                self.expect('LETTER')
                return identifier

            if self.current_token[0] == 'BOOLEAN':
                boolean = BoolLit(self.current_token[1])
                self.expect('BOOLEAN')
                return boolean

            if self.current_token[0] == 'LPAREN':
                self.expect('LPAREN')
                expr = self.parse_expression()
                self.expect('RPAREN')
                return expr

            self.error(
                f"Unexpected token: '{self.current_token[0]}' at line {self.current_token[2]}, column {self.current_token[3]}")

        def parse_operation(parse_func, valid_operators):
            left = parse_func()
            while self.current_token[0] in valid_operators:
                op = self.current_token[1]
                self.expect(self.current_token[0])
                right = parse_func()
                left = BinOp(left, op, right)
            return left

        return parse_operation(parse_term, {'BASIC_OP', 'BOOL_OP', 'COMP_OP'})
