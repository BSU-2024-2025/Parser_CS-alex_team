class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def eat(self, token_type, value=None):
        token = self.current_token()
        if token and token[0] == token_type and (value is None or token[1] == value):
            self.position += 1
            return token
        raise Exception(f"Unexpected token: {token}, expected: ({token_type}, {value})")

    def parse(self):
        return self.program()

    def program(self):
        return {
            'type': 'Program',
            'body': self.statement_list()
        }

    def statement_list(self):
        statements = []
        while self.current_token() and self.current_token()[1] != '}':
            statements.append(self.statement())
        return statements

    def statement(self):
        token = self.current_token()
        if token[0] == 'IDENTIFIER':
            if self.next_token_is('PUNCTUATION', '('):
                return self.function_call_statement()
            return self.assignment_statement()
        elif token[0] == 'KEYWORD':
            if token[1] == 'function':
                return self.function_definition()
            elif token[1] == 'print':
                return self.print_statement()
            elif token[1] == 'if':
                return self.if_statement()
            elif token[1] == 'while':
                return self.while_statement()
            elif token[1] == 'return':
                return self.return_statement()
        else:
            raise Exception(f"Unexpected token in statement: {token}")

    def assignment_statement(self):
        identifier = self.eat('IDENTIFIER')
        self.eat('OPERATOR', '=')
        expression = self.expression()
        self.eat('PUNCTUATION', ';')
        return {
            'type': 'AssignmentStatement',
            'left': identifier,
            'right': expression
        }

    def function_call_statement(self):
        call = self.function_call()
        self.eat('PUNCTUATION', ';')
        return {
            'type': 'FunctionCallStatement',
            'call': call
        }

    def function_definition(self):
        self.eat('KEYWORD', 'function')
        name = self.eat('IDENTIFIER')
        self.eat('PUNCTUATION', '(')
        parameters = self.parameter_list()
        self.eat('PUNCTUATION', ')')
        self.eat('PUNCTUATION', '{')
        body = self.statement_list()
        self.eat('PUNCTUATION', '}')
        return {
            'type': 'FunctionDefinition',
            'name': name,
            'parameters': parameters,
            'body': body
        }

    def parameter_list(self):
        parameters = []
        if self.current_token()[0] == 'IDENTIFIER':
            parameters.append(self.eat('IDENTIFIER'))
            while self.current_token() and self.current_token()[1] == ',':
                self.eat('PUNCTUATION', ',')
                parameters.append(self.eat('IDENTIFIER'))
        return parameters

    def print_statement(self):
        self.eat('KEYWORD', 'print')
        self.eat('PUNCTUATION', '(')
        expression = self.expression()
        self.eat('PUNCTUATION', ')')
        self.eat('PUNCTUATION', ';')
        return {
            'type': 'PrintStatement',
            'value': expression
        }

    def if_statement(self):
        self.eat('KEYWORD', 'if')
        self.eat('PUNCTUATION', '(')
        condition = self.expression()
        self.eat('PUNCTUATION', ')')
        self.eat('PUNCTUATION', '{')
        body = self.statement_list()
        self.eat('PUNCTUATION', '}')
        else_if_clauses = self.else_if_clauses()
        else_clause = self.else_clause()
        return {
            'type': 'IfStatement',
            'condition': condition,
            'body': body,
            'else_if_clauses': else_if_clauses,
            'else': else_clause
        }

    def else_if_clauses(self):
        else_if_clauses = []
        while self.current_token() and self.current_token()[1] == 'else':
            if self.next_token_is('KEYWORD', 'if'):
                else_if_clauses.append(self.else_if_clause())
            else:
                break
        return else_if_clauses

    def else_if_clause(self):
        self.eat('KEYWORD', 'else')
        self.eat('KEYWORD', 'if')
        self.eat('PUNCTUATION', '(')
        condition = self.expression()
        self.eat('PUNCTUATION', ')')
        self.eat('PUNCTUATION', '{')
        body = self.statement_list()
        self.eat('PUNCTUATION', '}')
        return {
            'type': 'ElseIfClause',
            'condition': condition,
            'body': body
        }

    def else_clause(self):
        if self.current_token() and self.current_token()[1] == 'else':
            self.eat('KEYWORD', 'else')
            self.eat('PUNCTUATION', '{')
            body = self.statement_list()
            self.eat('PUNCTUATION', '}')
            return body
        return None

    def while_statement(self):
        self.eat('KEYWORD', 'while')
        self.eat('PUNCTUATION', '(')
        condition = self.expression()
        self.eat('PUNCTUATION', ')')
        self.eat('PUNCTUATION', '{')
        body = self.statement_list()
        self.eat('PUNCTUATION', '}')
        return {
            'type': 'WhileStatement',
            'condition': condition,
            'body': body
        }

    def return_statement(self):
        self.eat('KEYWORD', 'return')
        expression = self.expression()
        self.eat('PUNCTUATION', ';')
        return {
            'type': 'ReturnStatement',
            'value': expression
        }

    def expression(self):
        node = self.term()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in {'+', '-', '>=', '<=', '==', '!=', '>', '<', '&&', '||'}:
            operator = self.eat('OPERATOR')
            right = self.term()
            node = {
                'type': 'BinaryExpression',
                'operator': operator,
                'left': node,
                'right': right
            }
        return node

    def term(self):
        node = self.factor()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in {'*', '/', '%', '//', '**'}:
            operator = self.eat('OPERATOR')
            right = self.factor()
            node = {
                'type': 'BinaryExpression',
                'operator': operator,
                'left': node,
                'right': right
            }
        return node

    def factor(self):
        token = self.current_token()
        if token[0] == 'NUMBER':
            return self.eat('NUMBER')
        elif token[0] == 'STRING':
            return self.eat('STRING')
        elif token[0] == 'BOOLEAN':
            return self.eat('BOOLEAN')
        elif token[0] == 'IDENTIFIER':
            if self.next_token_is('PUNCTUATION', '('):
                return self.function_call()
            return self.eat('IDENTIFIER')
        elif token[1] == '(':
            self.eat('PUNCTUATION', '(')
            expr = self.expression()
            self.eat('PUNCTUATION', ')')
            return expr
        elif token[0] == 'OPERATOR' and token[1] == '!':
            operator = self.eat('OPERATOR', '!')
            operand = self.factor()
            return {
                'type': 'UnaryExpression',
                'operator': operator,
                'operand': operand
            }
        raise Exception(f"Unexpected token in factor: {token}")

    def function_call(self):
        identifier = self.eat('IDENTIFIER')
        self.eat('PUNCTUATION', '(')
        arguments = self.argument_list()
        self.eat('PUNCTUATION', ')')
        return {
            'type': 'FunctionCall',
            'identifier': identifier,
            'arguments': arguments
        }

    def argument_list(self):
        arguments = []
        if self.current_token()[0] != 'PUNCTUATION' or self.current_token()[1] != ')':
            arguments.append(self.expression())
            while self.current_token() and self.current_token()[1] == ',':
                self.eat('PUNCTUATION', ',')
                arguments.append(self.expression())
        return arguments

    def next_token_is(self, token_type, value=None):
        if self.position + 1 < len(self.tokens):
            next_token = self.tokens[self.position + 1]
            if next_token[0] == token_type and (value is None or next_token[1] == value):
                return True
        return False
