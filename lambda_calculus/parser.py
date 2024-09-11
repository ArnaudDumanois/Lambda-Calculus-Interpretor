from lambda_calculus.lexer import Token
from lambda_calculus.core import Variable, Function, Application


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        return self.parse_expression()

    def parse_expression(self):
        # Parse either a function or an application
        left = self.parse_term()
        while self.peek(Token.VARIABLE) or self.peek(Token.LPAREN) or self.peek(Token.LAMBDA):
            right = self.parse_term()
            left = Application(left, right)
        return left

    def parse_function(self):
        self.consume(Token.LAMBDA)
        var = self.consume(Token.VARIABLE).value
        self.consume(Token.DOT)
        term = self.parse_expression()
        return Function(Variable(var), term)

    def parse_term(self):
        if self.peek(Token.VARIABLE):
            return Variable(self.consume(Token.VARIABLE).value)
        elif self.peek(Token.LPAREN):
            self.consume(Token.LPAREN)
            expr = self.parse_expression()
            self.consume(Token.RPAREN)
            return expr
        elif self.peek(Token.LAMBDA):
            return self.parse_function()
        else:
            raise SyntaxError("Expected variable or '('")

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
