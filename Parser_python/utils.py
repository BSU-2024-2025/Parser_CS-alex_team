from interpreter import Interpreter
from lexer import Lexer
from parser import Parser

class Utils:
    def __init__(self):
        self.interpreter = Interpreter()

    def run_expression(self, code: str) -> str:
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        output = self.capture_output(lambda: self.interpreter.evaluate(ast))
        return output

    def capture_output(self, func):
        import io
        import sys
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        try:
            func()
        finally:
            sys.stdout = old_stdout

        return new_stdout.getvalue()