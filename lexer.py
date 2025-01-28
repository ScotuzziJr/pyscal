from typing import Optional

from tokens import Token, TOKENS

class Lexer():
    def __init__(self, source: str) -> None:
        self.source = source # e.g: '3+5'
        self.pos = 0 # index of source
        self.current_char = self.source[self.pos]

    # auxiliary function
    def error(self) -> None:
        raise Exception('Lexical error: invalid character')

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
                return Token(TOKENS.INTEGER.name, self.integer())
            elif self.current_char == '+':
                self.advance()
                return Token(TOKENS.PLUS.name, '+')
            elif self.current_char == '-':
                self.advance()
                return Token(TOKENS.MINUS.name, '-')
            elif self.current_char == '/':
                self.advance()
                return Token(TOKENS.DIV.name, '/')
            elif self.current_char == '*':
                self.advance()
                return Token(TOKENS.MUL.name, '*')
            elif self.current_char == '(':
                self.advance()
                return Token(TOKENS.L_PAREN.name, '(')
            elif self.current_char == ')':
                self.advance()
                return Token(TOKENS.R_PAREN.name, ')')

            self.error()

        return Token(TOKENS.EOF.name, None)
