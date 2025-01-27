# Token Types
from typing_extensions import Optional, Union

INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

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

class Pyscal():
    def __init__(self, source: str) -> None:
        self.source = source # e.g: '3+5'
        self.pos = 0 # index of source
        self.current_token = None # current token instance
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

            self.error()

        return Token(EOF, None)

    def consume_token(self, token_type) -> None:
        """
        This method check the actual token type with the expected token type according to the grammar.
        If they match the token will be consumed and the current token instance will be updated by get_next_token() method.
        """
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self) -> Optional[int]:
        """
        This method evaluate expressions

        For now an expression is:
            expr -> INTEGER PLUS INTEGER
            expr -> INTEGER MINUS INTEGER
        """
        # current token becomes the first token from source
        self.current_token = self.get_next_token()

        # we expect the first operand to be an integer
        left = self.current_token
        self.consume_token(INTEGER)

        # we expect the operator to be a '+'
        op = self.current_token

        if op.type == PLUS:
            self.consume_token(PLUS)
        else:
            self.consume_token(MINUS)

        # we expect the second second to be an integer
        right = self.current_token
        self.consume_token(INTEGER)

        # EOF is the final token

        # If the code reaches this point its because all tokens has valid types
        if op.type == PLUS:
            return left.value + right.value
        else:
            return left.value - right.value

def run() -> None:
    while True:
        try:
            source = input('pyscal> ')
        except EOFError:
            break
        if not source:
           continue

        pyscal = Pyscal(source)
        result = pyscal.expr()
        print(result)

if __name__ == '__main__':
    run()
