## Overview

This project provides a simple interpreter for a custom programming language, including features like variable assignments, functions, conditionals (`if`, `else`), loops (`while`), and basic arithmetic operations.

The project consists of several modules:

- **Lexer**: Tokenizes the source code.
- **Parser**: Builds an Abstract Syntax Tree (AST) from the tokenized input.
- **Interpreter**: Evaluates the AST and executes the code.

The project is structured to allow expressions to be run dynamically, and the output of any evaluated code is captured and returned as a string.

## Files

### `utils.py`

The `Utils` class is a utility class that:

- Runs an expression by tokenizing the code, parsing it, and evaluating it.
- Captures the output of evaluated code and returns it as a string.

#### `Utils`

```python
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
```

### `interpreter.py`

The `Interpreter` class is responsible for evaluating an Abstract Syntax Tree (AST) and executing the code. It supports several types of statements and expressions, such as variable assignments, function definitions, arithmetic operations, and control flow (e.g., `if`, `while`).

#### `Interpreter`

```python
class Interpreter:
	def __init__(self):
		self.global_scope = {}
		self.environment = self.global_scope  # Initial global scope

	def evaluate(self, node):
		if isinstance(node, tuple):
			node = self.convert_tuple_to_node(node)
		method_name = f"evaluate_{node['type']}"
		method = getattr(self, method_name, self.generic_evaluate)
		return method(node)
```

### `lexer.py`

The `Lexer` class takes the source code as input and splits it into tokens. These tokens are then passed to the parser. The lexer recognizes various elements such as numbers, strings, identifiers, keywords, operators, and punctuation.

#### `Lexer`

```python
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

        if self.code[self.position:self.position+2] == "//":
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

        raise Exception(f"Invalid character '{self.code[self.position]}'")
```

### `parser.py`

The `Parser` class is responsible for converting a sequence of tokens into an Abstract Syntax Tree (AST). The parser can handle statements like assignments, function definitions, and control flow structures.

#### `Parser`

```python
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
```

## Key Concepts

### Lexer

- The `Lexer` class tokenizes the raw source code into tokens that can be processed by the parser.
- Tokens can represent numbers, strings, identifiers, keywords, operators, and punctuation.

### Parser

- The `Parser` class builds an Abstract Syntax Tree (AST) from the tokens produced by the lexer.
- The AST represents the logical structure of the code.

### Interpreter

- The `Interpreter` class evaluates the AST and executes the code.
- It supports various control flow structures, including assignments, functions, `if` statements, `while` loops, and binary expressions.

## Features

### Expressions

- Arithmetic operations (`+`, `-`, `*`, `/`, `**`, `%`)
- Boolean operations ( `==`, `!=`, `>`, `<`, `>=`, `<=`, `&&`, `||`)
- Unary operations (`!` for negation)

### Statements

- **Assignment**: `x = 5;`
- **Print**: `print(x);`
- **Function Definition**: `function f(a) { return a + 1; }`
- **Control Flow**: `if (x > 5) { ... }`, `while (x < 10) { ... }`

## Usage Example

```python
utils = Utils()
output = utils.run_expression('print(1 + 2);')
print(output)  # Expected output: 3
```

### Running the code

To run an expression, simply use the `run_expression` method of the `Utils` class, passing the code as a string. The method will evaluate the expression and return the output as a string.

## Conclusion

This project demonstrates how to build a simple interpreter for a custom programming language. The lexer converts the raw code into tokens, the parser constructs an AST, and the interpreter executes the code. You can extend this project by adding more features such as support for more complex data structures, error handling, or more advanced control flow mechanisms.
