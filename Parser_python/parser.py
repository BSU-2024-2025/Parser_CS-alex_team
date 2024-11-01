import unittest

OPERATOR_PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}

def precedence(op):
    """Return precedence level of an operator."""
    return OPERATOR_PRECEDENCE.get(op, 0)

def apply_operator(operators, values):
    """Apply an operator to the top two values in the stack."""
    operator = operators.pop()
    right = values.pop()
    left = values.pop()
    
    operations = {
        '+': left + right,
        '-': left - right,
        '*': left * right,
        '/': left / right
    }
    values.append(operations[operator])

def parse_number(expression, i):
    """Parse a number (integer or float) from expression starting at index i."""
    num = ''
    while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
        num += expression[i]
        i += 1
    return num, i - 1

def infix_to_postfix(expression, variables):
    """Convert infix expression to postfix notation, replacing variables with values."""
    operators, postfix = [], []
    i = 0
    while i < len(expression):
        if expression[i].isdigit() or expression[i] == '.':
            num, i = parse_number(expression, i)
            postfix.append(num)
        elif expression[i].isalpha():
            var = ''
            while i < len(expression) and expression[i].isalpha():
                var += expression[i]
                i += 1
            if var in variables:
                postfix.append(str(variables[var]))
            else:
                raise ValueError(f"Undefined variable: {var}")
            i -= 1
        elif expression[i] == '(':
            operators.append(expression[i])
        elif expression[i] == ')':
            while operators and operators[-1] != '(':
                postfix.append(operators.pop())
            operators.pop()  # Remove the '('
        elif expression[i] in OPERATOR_PRECEDENCE:
            while operators and precedence(operators[-1]) >= precedence(expression[i]):
                postfix.append(operators.pop())
            operators.append(expression[i])
        i += 1

    while operators:
        postfix.append(operators.pop())
    
    return postfix

def evaluate_postfix(postfix):
    """Evaluate a postfix expression and return the result."""
    stack = []
    for token in postfix:
        if token.replace('.', '', 1).isdigit():
            stack.append(float(token) if '.' in token else int(token))
        else:
            right = stack.pop()
            left = stack.pop()
            operations = {'+': left + right, '-': left - right, '*': left * right, '/': left / right}
            stack.append(operations[token])
    return stack[0]

def extract_variables(expression):
    """Extract variables from the start of the expression string."""
    variables = {}
    parts = expression.split()
    for i, part in enumerate(parts):
        if '=' in part:
            var, value = part.split('=')
            variables[var] = float(value) if '.' in value else int(value)
        else:
            # Stop if we encounter the start of the actual expression
            return variables, ' '.join(parts[i:])
    return variables, ''

def evaluate_expression(expression):
    """Evaluate an arithmetic expression with variables defined in the start of the string."""
    variables, expression = extract_variables(expression)
    postfix = infix_to_postfix(expression, variables)
    return evaluate_postfix(postfix)

def is_valid_expression(expression):
    """Проверяет, является ли выражение допустимым, учитывая сбалансированные скобки, отсутствие пустых скобок и операторов подряд."""
    stack = []
    operators = {'+', '-', '*', '/'}
    previous_char = None
    
    # Убираем комментарии и пустые строки
    expression = ' '.join(line.split('//')[0].strip() for line in expression.splitlines() if line.strip())
    
    for i, char in enumerate(expression.replace(' ', '')):
        if char == '(':
            # Check for empty parentheses immediately following '('
            if i + 1 < len(expression) and expression[i + 1] == ')':
                return False
            stack.append(char)
        elif char == ')':
            if not stack or stack.pop() != '(':
                return False
            # Ensure no operator directly precedes a closing parenthesis
            if previous_char in operators:
                return False
        elif char in operators:
            if previous_char in operators or previous_char == '(':
                return False
        previous_char = char
    
    # If stack is empty, parentheses are balanced
    return not stack



class TestExpressionEvaluator(unittest.TestCase):
    def test_valid_expressions(self):
        self.assertTrue(is_valid_expression("3 + (2 - 5) * 2"))
        self.assertTrue(is_valid_expression("2 * (3 + 5) / (7 - (2 + 4))"))
    
    def test_invalid_expressions(self):
        self.assertFalse(is_valid_expression("(3 + 2))"))
        self.assertFalse(is_valid_expression("3 + ()"))
        self.assertFalse(is_valid_expression("3 + - 2"))
        self.assertFalse(is_valid_expression("4 * / 2"))

    
    def test_no_brackets(self):
        self.assertTrue(is_valid_expression("3 + 2 - 5 * 4"))
    
    def test_with_comments_and_empty_lines(self):
        expression = """
        // This is a comment
        3 + (2 - 5) * 2  // another comment
        // Blank line above
        """
        self.assertTrue(is_valid_expression(expression))
    
    def test_evaluate_expression_without_variables(self):
        expression = "3 + (2 - 5) * 2"
        self.assertEqual(evaluate_expression(expression), 3 + (2 - 5) * 2)
    
    def test_evaluate_expression_with_variables_in_string(self):
        expression = "x=5 y=3 3 + (x - y) * 2"
        self.assertEqual(evaluate_expression(expression), 3 + (5 - 3) * 2)
    
    def test_evaluate_expression_with_undefined_variable(self):
        expression = "3 + z"
        with self.assertRaises(ValueError):
            evaluate_expression(expression)

if __name__ == "__main__":
    unittest.main()
