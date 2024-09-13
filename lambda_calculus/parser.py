from lambda_calculus.lexer import Token
from lambda_calculus.core import Variable, Function, Application
from collections import deque

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        return self.parse_expression()

    def parse_expression(self):
        stack = deque()
        while self.pos < len(self.tokens):
            if self.peek(Token.VARIABLE):
                stack.append(self.parse_variable())
            elif self.peek(Token.LPAREN):
                stack.append(self.parse_parentheses())
            elif self.peek(Token.LAMBDA):
                stack.append(self.parse_function())
            else:
                break

            if len(stack) >= 2:
                arg = stack.pop()
                func = stack.pop()
                stack.append(Application(func, arg))

        if not stack:
            raise SyntaxError("Empty expression")
        return stack.pop()

    def parse_variable(self):
        token = self.consume(Token.VARIABLE)
        return Variable(token.value)

    def parse_parentheses(self):
        self.consume(Token.LPAREN)
        expr = self.parse_expression()
        self.consume(Token.RPAREN)
        return expr

    def parse_function(self):
        self.consume(Token.LAMBDA)
        var = self.consume(Token.VARIABLE).value
        self.consume(Token.DOT)
        term = self.parse_expression()
        return Function(Variable(var), term)

    def peek(self, token_type):
        return self.pos < len(self.tokens) and self.tokens[self.pos].type == token_type

    def consume(self, token_type):
        if self.peek(token_type):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        else:
            raise SyntaxError(f"Expected {token_type}, found {self.tokens[self.pos].type}")

    def print_expression(self, expr):
        if isinstance(expr, Variable):
            return f'Variable({expr.name})'
        elif isinstance(expr, Function):
            return f'Function({self.print_expression(expr.var)}, {self.print_expression(expr.term)})'
        elif isinstance(expr, Application):
            return f'Application({self.print_expression(expr.func)}, {self.print_expression(expr.arg)})'
        return expr