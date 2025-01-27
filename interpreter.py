from parser import Parser

class Interpreter:
    def __init__(self, source: str) -> None:
        self.source = source

    def run(self):
        parser = Parser(self.source)

        return parser.expr()
