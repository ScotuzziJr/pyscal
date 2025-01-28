from interpreter import Interpreter
from lexer import Lexer
from parser import Parser

while True:
    try:
        source = input('pyscal> ')
    except EOFError:
        break

    if not source:
        continue
    elif source == 'q':
        break

    lexer = Lexer(source)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.run()
    print(result)
