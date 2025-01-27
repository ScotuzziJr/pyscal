# Token Types
from typing_extensions import Optional, Union

INTEGER, PLUS, MINUS, DIV, MULT, EOF = 'INTEGER', 'PLUS', 'MINUS', 'DIV', 'MULT', 'EOF'

class Token():
    def __init__(self, type: str, value: Optional[Union[int, str]]) -> None:
        # Token Type: INTEGER, PLUS or EOF
        self.type = type
        # Token Value: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+' or None
        self.value = value

    def __str__(self) -> str:
        return f'Token({self.type}, {self.value}))'

    def __repr__(self) -> str:
        return self.__str__()

class Lexer():
    def __init__(self, source: str) -> None:
        self.source = source # e.g: '3+5'
        self.pos = 0 # index of source
        self.current_char = self.source[self.pos]

    # auxiliary function
    def error(self) -> None:
        raise Exception('Error parsing input')

    def advance(self) -> None:
        """
        This method advances the 'pos' pointer and set the 'current_char' variable
        """
        self.pos += 1

        if self.pos > len(self.source) - 1:
            self.current_char = None
        else:
            self.current_char = self.source[self.pos]

    def skip_white_space(self) -> None:
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self) -> int:
        """
        This method returns an integer consumed from the input (single or multidigit)
        """
        integer = ''

        while self.current_char is not None and self.current_char.isdigit():
            integer += self.current_char
            self.advance()

        return int(integer)

    def get_next_token(self) -> Optional[Token]:
        """
        Lexer analyzer

        This method breaks the input (source code) into tokens.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_white_space()
                continue
            elif self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            elif self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            elif self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            elif self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            elif self.current_char == '*':
                self.advance()
                return Token(MULT, '*')

            self.error()

        return Token(EOF, None)

class Pyscal():
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token() # current token instance

    def consume_token(self, token_type) -> None:
        """
        This method check the actual token type with the expected token type according to the grammar.
        If they match the token will be consumed and the current token instance will be updated by get_next_token() method.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.lexer.error()

    def factor(self) -> None:
        """
        factor : INTEGER
        """
        token = self.current_token
        self.consume_token(INTEGER)
        return token.value

    def term(self) -> None:
        """
        term: factor ((MULT | DIV) factor)*
        """
        result = self.factor()

        while self.current_token.type in (MULT, DIV):
            token = self.current_token

            if token.type == MULT:
                self.consume_token(MULT)
                result *= self.factor()
            elif token.type == DIV:
                self.consume_token(DIV)
                result /= self.factor()

        return result

    def expr(self) -> Optional[Union[int, float]]:
        """
        Parser / Interpreter

        pyscal>  14 + 2 * 3 - 6 / 2
                17

        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MULT | DIV) factor)*
        factor : INTEGER
        """
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token

            if token.type == PLUS:
                self.consume_token(PLUS)
                result += self.term()
            elif token.type == MINUS:
                self.consume_token(MINUS)
                result -= self.term()

        return result

def run() -> None:
    while True:
        try:
            source = input('pyscal> ')
        except EOFError:
            break
        if not source:
           continue

        lexer = Lexer(source)
        pyscal = Pyscal(lexer)
        result = pyscal.expr()
        print(result)

if __name__ == '__main__':
    run()
