from ast import BinOp, NodeVisitor
from parser import Parser
from tokens import TOKENS

class Interpreter(NodeVisitor):
    def __init__(self, parser: Parser) -> None:
        self.parser = parser

    def visit_BinOp(self, node: BinOp):
        if node.op.type == TOKENS.PLUS.name:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TOKENS.MINUS.name:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TOKENS.MUL.name:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TOKENS.DIV.name:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.lexeme

    def run(self):
        tree = self.parser.parse()

        return self.visit(tree)
