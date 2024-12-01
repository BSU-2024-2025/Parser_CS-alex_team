class Interpreter:
    def __init__(self):
        self.global_scope = {}
        self.environment = self.global_scope  # Начальная область видимости - глобальная

    def evaluate(self, node):
        if isinstance(node, tuple):
            node = self.convert_tuple_to_node(node)
        method_name = f"evaluate_{node['type']}"
        method = getattr(self, method_name, self.generic_evaluate)
        return method(node)

    def convert_tuple_to_node(self, node_tuple):
        node_type, node_value = node_tuple
        return {'type': node_type, 'value': node_value}

    def generic_evaluate(self, node):
        raise Exception(f"No evaluate_{node['type']} method")

    def evaluate_Program(self, node):
        for statement in node['body']:
            result = self.evaluate(statement)
            if isinstance(result, dict) and result.get('type') == 'ReturnStatement':
                return result['value']

    def evaluate_AssignmentStatement(self, node):
        identifier = node['left'][1]
        value = self.evaluate(node['right'])
        self.environment[identifier] = value

    def evaluate_PrintStatement(self, node):
        value = self.evaluate(node['value'])
        print(value)

    def evaluate_WhileStatement(self, node):
        while self.evaluate(node['condition']):
            result = self.evaluate_Program({'type': 'Program', 'body': node['body']})
            if isinstance(result, dict) and result.get('type') == 'ReturnStatement':
                return result['value']

    def evaluate_IfStatement(self, node):
        if self.evaluate(node['condition']):
            return self.evaluate_Program({'type': 'Program', 'body': node['body']})
        for else_if in node.get('else_if_clauses', []):
            if self.evaluate(else_if['condition']):
                return self.evaluate_Program({'type': 'Program', 'body': else_if['body']})
        if node.get('else'):
            return self.evaluate_Program({'type': 'Program', 'body': node['else']})

    def evaluate_BinaryExpression(self, node):
        left = self.evaluate(node['left'])
        right = self.evaluate(node['right'])
        operator = node['operator'][1]

        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            return left / right
        elif operator == '%':
            return left % right
        elif operator == '//':
            return left // right  # Целочисленное деление
        elif operator == '**':
            return left ** right
        elif operator == '==':
            return left == right
        elif operator == '!=':
            return left != right
        elif operator == '<':
            return left < right
        elif operator == '>':
            return left > right
        elif operator == '<=':
            return left <= right
        elif operator == '>=':
            return left >= right
        elif operator == '&&':
            return left and right
        elif operator == '||':
            return left or right
        else:
            raise Exception(f"Unsupported operator {operator}")

    def evaluate_UnaryExpression(self, node):
        operator = node['operator'][1]
        operand = self.evaluate(node['operand'])
        if operator == '!':
            return not operand
        else:
            raise Exception(f"Unsupported unary operator: {operator}")

    def evaluate_FunctionCallStatement(self, node):
        self.evaluate(node['call'])

    def evaluate_FunctionDefinition(self, node):
        name = node['name'][1]
        self.global_scope[name] = {
            'parameters': node['parameters'],
            'body': node['body']
        }

    def evaluate_FunctionCall(self, node):
        function_name = node['identifier'][1]
        if function_name not in self.global_scope:
            raise Exception(f"Undefined function: {function_name}")
        function = self.global_scope[function_name]

        arguments = [self.evaluate(arg) for arg in node['arguments']]
        parameters = [param[1] for param in function['parameters']]
        if len(arguments) != len(parameters):
            raise Exception(f"Argument count mismatch for function {function_name}")

        local_scope = {key: self.environment[key] for key in self.environment}
        local_scope.update(dict(zip(parameters, arguments)))

        previous_scope = self.environment
        self.environment = local_scope
        result = None
        try:
            for statement in function['body']:
                result = self.evaluate(statement)
                if isinstance(result, dict) and result.get('type') == 'ReturnStatement':
                    result = result['value']
                    break
        finally:
            self.environment = previous_scope
        return result

    def evaluate_ReturnStatement(self, node):
        return {
            'type': 'ReturnStatement',
            'value': self.evaluate(node['value'])
        }

    def evaluate_IDENTIFIER(self, node):
        identifier = node['value']
        if identifier in self.environment:
            return self.environment[identifier]
        elif identifier in self.global_scope:
            return self.global_scope[identifier]
        else:
            raise Exception(f"Undefined identifier: {identifier}")

    def evaluate_NUMBER(self, node):
        return node['value']

    def evaluate_STRING(self, node):
        return node['value']

    def evaluate_BOOLEAN(self, node):
        return node['value'] == 'true'
