class AstNode:
    # Base class for all AST nodes
    pass


class LambdaExpr(AstNode):
    def __init__(self, parameters, expr_body):
        self.parameters = parameters
        self.expr_body = expr_body

    def __repr__(self):
        return f"lambda_expr(parameters={self.parameters}, expr_body={self.expr_body})"


class FuncDef(AstNode):
    def __init__(self, func_name, parameters, func_body):
        self.func_name = func_name
        self.parameters = parameters
        self.func_body = func_body

    def __repr__(self):
        return f"func_def(func_name={self.func_name}, parameters={self.parameters}, func_body={self.func_body})"


class IfStmt(AstNode):
    def __init__(self, cond, then_branch, else_branch=None):
        self.cond = cond
        self.then_branch = then_branch  # do if true
        self.else_branch = else_branch  # do if false

    def __repr__(self):
        return f"if_stmt(cond={self.cond}, then_branch={self.then_branch}, else_branch={self.else_branch})"


class FuncApp(AstNode):
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments

    def __repr__(self):
        return f"func_app(function={self.function}, arguments={self.arguments})"


class BinOp(AstNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"bin_op(lhs={self.left}, op={self.op}, rhs={self.right})"


class UnaryOp(AstNode):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f"unary_op(op={self.op}, operand={self.operand})"


class IntLit(AstNode):
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f"int_lit(val={self.val})"


class Identifier(AstNode):
    def __init__(self, id_name):
        self.id_name = id_name

    def __repr__(self):
        return f"identifier(id_name={self.id_name})"


class BoolLit(AstNode):
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f"bool_lit(val={self.val})"
