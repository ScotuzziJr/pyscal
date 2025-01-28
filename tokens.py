from enum import Enum
from typing import Union, Optional

TOKENS = Enum("TOKENS", [
    "EOF",
    "INTEGER",
    "PLUS",
    "MINUS",
    "MUL",
    "DIV",
    "L_PAREN",
    "R_PAREN"
])

class Token:
    def __init__(self, type: str, lexeme: Optional[Union[int, str]]) -> None:
        self.type = type
        self.lexeme = lexeme

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.lexeme})"
