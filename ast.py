from tokens import Token

class AST:
    pass

class BinOp(AST):
    def __init__(self, left: int, op: str, right: int) -> None:
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token: Token) -> None:
        self.token = token.type
        self.lexeme = token.lexeme

class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')
