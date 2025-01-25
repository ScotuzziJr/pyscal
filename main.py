# Token Types
from typing_extensions import Optional, Union


INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

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

    # auxiliary function
    def error(self) -> None:
        raise Exception('Error parsing input')

    def get_next_token(self) -> Optional[Token]:
        """
        Lexer analyzer

        This method breaks the input (source code) into tokens.
        """
        source = self.source

        # check if the lexer read every character of the source code
        # if it read then will return EOF (end of file)
        if self.pos > len(source) - 1:
            return Token(EOF, None)

        current_char = source[self.pos]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        elif current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        self.error()

    def advance(self, token_type: str) -> None:
        """
        This method perform type checking on token and calls the get_next_token function if types are matching
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
        """
        # current token becomes the first token from source
        self.current_token = self.get_next_token()

        # we expect the first operand to be an integer
        left = self.current_token
        self.advance(INTEGER)

        # we expect the operator to be a '+'
        op = self.current_token
        self.advance(PLUS)

        # we expect the second second to be an integer
        right = self.current_token
        self.advance(INTEGER)

        # EOF is the final token

        # If the code reaches this point its because all tokens has valid types
        return left.value + right.value

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
