from ast_node import FuncDef, LambdaExpr, FuncApp, Identifier, IntLit, BoolLit, UnaryOp, BinOp, IfStmt


class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.context = {}

    def define(self, name, value):
        self.context[name] = value

    def extend_scope(self, names, values):
        child = Environment(self)
        for name, value in zip(names, values):
            child.define(name, value)
        return child

    def get(self, name):
        if name in self.context:
            return self.context[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Undefined variable: {name}")


class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.global_env = Environment()

    def interpret(self):
        print("Starting the interpretation - ")
        try:
            result = None
            for node in self.ast:
                try:
                    result = self.evaluate(node, self.global_env)
                    if result is not None:
                        print(result)
                except Exception as e:
                    print(f"Error during the interpretation of node {node}: {e}")
            print("Interpretation is finished -")
            return result
        except Exception as e:
            raise RuntimeError(f"Runtime error during the interpretation: {str(e)}")

    def evaluate(self, node, context):
        if isinstance(node, IntLit):
            return node.val

        elif isinstance(node, Identifier):
            return context.get(node.id_name)

        elif isinstance(node, BoolLit):
            return node.val

        elif isinstance(node, UnaryOp):
            value = self.evaluate(node.operand, context)
            return self.apply_unary_operator(node.op, value)

        elif isinstance(node, BinOp):
            left = self.evaluate(node.left, context)
            if node.op == '||' and left:
                return True
            if node.op == '&&' and not left:
                return False
            right = self.evaluate(node.right, context)
            return self.apply_operators(node.op, left, right)

        elif isinstance(node, LambdaExpr):
            return node.parameters, node.expr_body, context

        elif isinstance(node, FuncDef):
            context.set(node.func_name, (node.parameters, node.func_body, context))
            return None

        elif isinstance(node, IfStmt):
            try:
                condition_value = self.evaluate(node.cond, context)
                if condition_value:
                    return self.evaluate(node.then_branch, context)
                elif node.else_branch is not None:
                    return self.evaluate(node.else_branch, context)
                return None
            except Exception as e:
                raise RuntimeError(f"Error evaluating if-statement: {str(e)}")

        elif isinstance(node, FuncApp):
            try:
                if isinstance(node.function, str):
                    func = context.get(node.function)
                else:
                    func = self.evaluate(node.function, context)

                args = [self.evaluate(arg, context) for arg in node.arguments]
                if isinstance(func, tuple) and len(func) == 3:
                    parameters, body, closure_env = func

                    if isinstance(parameters, list):
                        if len(parameters) != len(args):
                            raise TypeError(f"Function expected {len(parameters)} arguments but got {len(args)}")

                        new_env = closure_env.extend_scope(parameters, args)
                        return self.evaluate(body, new_env)
                    else:  # Lambda expression
                        for arg in args:
                            func = self.execute_function(func, [arg])
                        return func

                else:
                    raise TypeError(f"Expected a function or lambda expression, but got: {func}")

            except Exception as e:
                raise RuntimeError(f"Error applying function: {str(e)}")

        else:
            raise TypeError(f"Unknown node type: {type(node)}")

    def execute_function(self, function, arguments):
        parameters, body, closure_basic = function

        if len(arguments) != 1:
            raise TypeError("Each lambda expression should receive exactly one argument.")

        new_basic = closure_basic.extend_scope([parameters], arguments)
        result = self.evaluate(body, new_basic)
        return result

    def apply_operators(self, op, left, right):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            if right == 0:
                raise ZeroDivisionError("Invalid, division by zero!")
            return left // right
        elif op == '%':
            return left % right
        elif op == '||':
            return left or right
        elif op == '&&':
            return left and right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        else:
            raise TypeError(f"Invalid operator: {op}")

    def apply_unary_operator(self, op, value):
        if op == '!':
            return not value
        else:
            raise TypeError(f"invalid unary operator: {op}")
