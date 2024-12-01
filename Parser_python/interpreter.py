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
        identifier = node['left'][1]  # Получаем имя идентификатора из ('IDENTIFIER', 'name')
        value = self.evaluate(node['right'])  # Оцениваем выражение справа
        self.environment[identifier] = value  # Сохраняем значение в текущей области видимости

    def evaluate_FunctionDefinition(self, node):
        name = node['name'][1]  # 'fff'
        function_object = {
            'type': 'Function',
            'parameters': node['parameters'],
            'body': node['body']
        }
        self.global_scope[name] = function_object  # Сохраняем функцию в глобальной области видимости

    def evaluate_PrintStatement(self, node):
        value = self.evaluate(node['value'])
        print(value)

    def evaluate_IfStatement(self, node):
        condition = self.evaluate(node['condition'])
        result = None  # Убедимся, что result определена
        if condition:
            result = self.evaluate_Program({'type': 'Program', 'body': node['body']})
        else:
            for else_if_clause in node['else_if_clauses']:
                condition = self.evaluate(else_if_clause['condition'])
                if condition:
                    result = self.evaluate_Program({'type': 'Program', 'body': else_if_clause['body']})
                    break
            if node['else'] is not None and result is None:
                result = self.evaluate_Program({'type': 'Program', 'body': node['else']})
        return result

    def evaluate_WhileStatement(self, node):
        condition = self.evaluate(node['condition'])
        while condition:
            result = self.evaluate_Program({'type': 'Program', 'body': node['body']})
            if isinstance(result, dict) and result.get('type') == 'ReturnStatement':
                return result['value']
            condition = self.evaluate(node['condition'])

    def evaluate_ReturnStatement(self, node):
        return {'type': 'ReturnStatement', 'value': self.evaluate(node['value'])}

    def evaluate_BinaryExpression(self, node):
        left = self.evaluate(node['left'])
        right = self.evaluate(node['right'])
        operator = node['operator'][1]  # Извлекаем оператор напрямую (например, '+')

        if operator == '+':
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            if isinstance(left, str) and isinstance(right, int):
                return left * right
            return left * right
        elif operator == '/':
            return left / right
        elif operator == '%':
            return left % right
        elif operator == '**':  # Возведение в степень
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
        operator = node['operator'][1]  # Извлекаем оператор напрямую (например, '!')
        operand = self.evaluate(node['operand'])
        if operator == '!':
            return not operand
        else:
            raise Exception(f"Unsupported unary operator: {operator}")

    def evaluate_FunctionCall(self, node):
        function_name = node['identifier'][1]  # 'fff'
        if function_name not in self.global_scope:
            raise Exception(f"Undefined function: {function_name}")
        function = self.global_scope[function_name]

        arguments = [self.evaluate(arg) for arg in node['arguments']]
        parameters = [param[1] for param in function['parameters']]
        if len(arguments) != len(parameters):
            raise Exception(f"Argument count mismatch for function {function_name}")

        # Создаем новую локальную область видимости для функции
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

    def evaluate_FunctionBody(self, body, local_scope):
        previous_scope = self.environment
        self.environment = local_scope
        result = None
        try:
            for statement in body:
                result = self.evaluate(statement)
                if isinstance(result, dict) and result.get('type') == 'ReturnStatement':
                    result = result['value']
                    break
        finally:
            self.environment = previous_scope
        return result

    def evaluate_NUMBER(self, node):
        return node['value']

    def evaluate_STRING(self, node):
        return node['value']

    def evaluate_IDENTIFIER(self, node):
        identifier = node['value']
        if identifier in self.environment:
            return self.environment[identifier]
        elif identifier in self.global_scope:
            return self.global_scope[identifier]
        else:
            raise Exception(f"Undefined identifier: {identifier}")

    def evaluate_BOOLEAN(self, node):
        return node['value'] == 'true'

