import re

KEYWORDS = {'if', 'else', 'while', 'print', 'function', 'return', 'true', 'false'}
OPERATORS = {'+', '-', '*', '/', '>=', '<=', '==', '!=', '=', '>', '<', '&&', '||', '!', '**', '//'}

PUNCTUATION = {'(', ')', '{', '}', ';', ','}

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.tokens = []

    def get_next_token(self):
        if self.position >= len(self.code):
            return None

        while self.position < len(self.code) and self.code[self.position].isspace():
            self.position += 1
        
        if self.position >= len(self.code):
            return None

        # Изменение для обработки комментариев
        if self.code[self.position] == '#':
            self.position = self.code.find("\n", self.position)
            return self.get_next_token()

        match = re.match(r'-?\d+\.\d+', self.code[self.position:])
        if match:
            value = float(match.group(0))
            self.position += len(match.group(0))
            return ('NUMBER', value)

        match = re.match(r'-?\d+', self.code[self.position:])
        if match:
            value = int(match.group(0))
            self.position += len(match.group(0))
            return ('NUMBER', value)

        match = re.match(r'"[^"]*"', self.code[self.position:])
        if match:
            value = match.group(0)[1:-1]
            self.position += len(match.group(0))
            return ('STRING', value)

        match = re.match(r'[a-zA-Z_][a-zA-Z_0-9]*', self.code[self.position:])
        if match:
            value = match.group(0)
            self.position += len(value)
            if value in KEYWORDS:
                return ('KEYWORD', value)
            else:
                return ('IDENTIFIER', value)

        for operator in sorted(OPERATORS, key=len, reverse=True):
            if self.code[self.position:self.position+len(operator)] == operator:
                self.position += len(operator)
                return ('OPERATOR', operator)

        if self.code[self.position] in PUNCTUATION:
            value = self.code[self.position]
            self.position += 1
            return ('PUNCTUATION', value)

        raise Exception(f"Недопустимый символ '{self.code[self.position]}'")

    def tokenize(self):
        while True:
            token = self.get_next_token()
            if not token:
                break
            self.tokens.append(token)
        return self.tokens
