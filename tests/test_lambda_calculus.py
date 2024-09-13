import unittest
from lambda_calculus.core import Variable, Function, Application
from lambda_calculus.lexer import lexer, Token
from lambda_calculus.parser import Parser
from lambda_calculus.evaluator import Evaluator
from lambda_calculus.church_arithmetic import church_numeral, church_add, church_multiply

class CoreTests(unittest.TestCase):
    def test_variable(self):
        x = Variable('x')
        self.assertEqual(x, Variable('x'))
        self.assertNotEqual(x, Variable('y'))
        self.assertEqual(hash(x), hash(Variable('x')))
        self.assertEqual(x(), x)

    def test_function(self):
        x, y = Variable('x'), Variable('y')
        f = Function(x, x)
        self.assertEqual(f, Function(x, x))
        self.assertNotEqual(f, Function(x, y))

    def test_application(self):
        x, y = Variable('x'), Variable('y')
        f = Function(x, x)
        app = Application(f, y)
        self.assertEqual(app, Application(f, y))
        self.assertNotEqual(app, Application(f, x))

class LexerTests(unittest.TestCase):
    def test_simple_lambda(self):
        input_str = "λx.(x y)"
        expected_tokens = [
            Token(Token.LAMBDA), Token(Token.VARIABLE, 'x'), Token(Token.DOT),
            Token(Token.LPAREN), Token(Token.VARIABLE, 'x'),
            Token(Token.VARIABLE, 'y'), Token(Token.RPAREN)
        ]
        self.assertEqual(lexer(input_str), expected_tokens)

    def test_nested_lambda(self):
        input_str = "λx.λy.x"
        expected_tokens = [
            Token(Token.LAMBDA), Token(Token.VARIABLE, 'x'), Token(Token.DOT),
            Token(Token.LAMBDA), Token(Token.VARIABLE, 'y'), Token(Token.DOT),
            Token(Token.VARIABLE, 'x')
        ]
        self.assertEqual(lexer(input_str), expected_tokens)

class ParserTests(unittest.TestCase):
    def parse_and_check(self, input_str, expected_expr):
        tokens = lexer(input_str)
        parser = Parser(tokens)
        parsed_expr = parser.parse()
        self.assertEqual(parsed_expr, expected_expr)

    def test_simple_lambda(self):
        self.parse_and_check(
            "λx.(x y)",
            Function(Variable('x'), Application(Variable('x'), Variable('y')))
        )

    def test_nested_lambda(self):
        self.parse_and_check(
            "λx.λy.x",
            Function(Variable('x'), Function(Variable('y'), Variable('x')))
        )

    def test_lambda_application(self):
        self.parse_and_check(
            "λx.λy.x y",
            Function(Variable('x'), Function(Variable('y'), Application(Variable('x'), Variable('y'))))
        )

class EvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.evaluator = Evaluator()

    def reduce_and_check(self, input_str, expected_expr):
        tokens = lexer(input_str)
        parser = Parser(tokens)
        expr = parser.parse()
        reduced_expr = self.evaluator.reduce(expr)
        self.assertEqual(reduced_expr, expected_expr)

    def test_identity(self):
        self.reduce_and_check(
            "(λx.x) y",
            Variable('y')
        )

    def test_constant_function(self):
        self.reduce_and_check(
            "(λx.λy.x) a b",
            Variable('a')
        )

    def test_omega(self):
        input_str = "(λx.x x) (λx.x x)"
        tokens = lexer(input_str)
        parser = Parser(tokens)
        expr = parser.parse()
        reduced_expr = self.evaluator.reduce(expr)
        self.assertEqual(reduced_expr, expr)  # Omega reduces to itself

    def test_beta_redex_under_lambda(self):
        self.reduce_and_check(
            "λy.((λx.x) y)",
            Function(Variable('y'), Variable('y'))
        )

class ChurchArithmeticTests(unittest.TestCase):
    def setUp(self):
        self.evaluator = Evaluator()


    def test_church_numerals(self):
        for n in range(20):
            church_n = church_numeral(n)
            expected_expr = f"λf.λx.{('f ' * n)}x"
            tokens = lexer(expected_expr)
            parser = Parser(tokens)
            expected_expr = self.evaluator.reduce(parser.parse())
            self.assertEqual(str(church_n), str(expected_expr))

    def test_church_to_int(self):
        for n in range(50):
            church_n = church_numeral(n)
            self.assertEqual(self.evaluator.church_to_int(church_n), n)


if __name__ == '__main__':
    unittest.main()