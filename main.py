from interpreter import Interpreter

while True:
    try:
        source = input('pyscal> ')
    except EOFError:
        break

    if not source:
        continue
    elif source == 'q':
        break

    interpreter = Interpreter(source)
    result = interpreter.run()
    print(result)
