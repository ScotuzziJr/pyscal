from typing import Union, Optional
from tokens import TOKENS
from lexer import Lexer

class Parser:
    def __init__(self, source) -> None:
        self.lexer = Lexer(source)
        self.current_token = self.lexer.get_next_token()

    def error(self):
            raise Exception('Parsing error: invalid syntax')

    def consume_token(self, token_type) -> None:
        """
        This method check the actual token type with the expected token type according to the grammar.
        If they match the token will be consumed and the current token instance will be updated by get_next_token() method.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self) -> None:
        """
        factor : INTEGER
        """
        token = self.current_token
        self.consume_token(TOKENS.INTEGER.name)
        return token.lexeme

    def term(self) -> None:
        """
        term: factor ((MULT | DIV) factor)*
        """
        result = self.factor()

        while self.current_token.type in (TOKENS.MUL.name, TOKENS.DIV.name):
            token = self.current_token

            if token.type == TOKENS.MUL.name:
                self.consume_token(TOKENS.MUL.name)
                result *= self.factor()
            elif token.type == TOKENS.DIV.name:
                self.consume_token(TOKENS.DIV.name)
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

        while self.current_token.type in (TOKENS.PLUS.name, TOKENS.MINUS.name):
            token = self.current_token

            if token.type == TOKENS.PLUS.name:
                self.consume_token(TOKENS.PLUS.name)
                result += self.term()
            elif token.type == TOKENS.MINUS.name:
                self.consume_token(TOKENS.MINUS.name)
                result -= self.term()

        return result
