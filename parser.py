from ast import Num, BinOp
from typing import Union, Optional
from tokens import TOKENS
from lexer import Lexer

class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
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

    def factor(self) -> Optional[Union[int, float]]:
        """
        factor : INTEGER | LPAREN expr RPAREN
        """
        token = self.current_token

        if token.type == TOKENS.INTEGER.name:
            self.consume_token(TOKENS.INTEGER.name)
            return Num(token)
        elif token.type == TOKENS.L_PAREN.name:
            self.consume_token(TOKENS.L_PAREN.name)
            node = self.expr()
            self.consume_token(TOKENS.R_PAREN.name)
            return node

    def term(self) -> None:
        """
        term: factor ((MULT | DIV) factor)*
        """
        node = self.factor()

        while self.current_token.type in (TOKENS.MUL.name, TOKENS.DIV.name):
            token = self.current_token

            if token.type == TOKENS.MUL.name:
                self.consume_token(TOKENS.MUL.name)
            elif token.type == TOKENS.DIV.name:
                self.consume_token(TOKENS.DIV.name)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self) -> Optional[Union[int, float, BinOp]]:
        """
        Parser / Interpreter

        pyscal>  14 + 2 * 3 - 6 / 2
                17

        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.type in (TOKENS.PLUS.name, TOKENS.MINUS.name):
            token = self.current_token

            if token.type == TOKENS.PLUS.name:
                self.consume_token(TOKENS.PLUS.name)
            elif token.type == TOKENS.MINUS.name:
                self.consume_token(TOKENS.MINUS.name)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):
        return self.expr()
