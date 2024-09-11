import unittest
from lambda_calculus.core import Variable, Function, Application
from lambda_calculus.lexer import lexer, Token
from lambda_calculus.parser import Parser
from lambda_calculus.evaluator import Evaluator


class LambdaCalculusTests(unittest.TestCase):

    def test_variable(self):
        x = Variable('x')
        print("Testing Variable:")
        print("Variable x:", x)
        print("String representation:", str(x))
        print("Repr representation:", repr(x))
        self.assertEqual(x, Variable('x'))
        self.assertNotEqual(x, Variable('y'))
        self.assertEqual(hash(x), hash(Variable('x')))
        self.assertEqual(x(), x)

    def test_function(self):
        x = Variable('x')
        f = Function(x, x)
        print("Testing Function:")
        print("Function f:", f)
        print("String representation:", str(f))
        print("Repr representation:", repr(f))
        self.assertEqual(f, Function(x, x))
        self.assertNotEqual(f, Function(x, Variable('y')))

    def test_application(self):
        x = Variable('x')
        y = Variable('y')
        f = Function(x, x)
        app = Application(f, y)
        print("Testing Application:")
        print("Application app:", app)
        print("String representation:", str(app))
        print("Repr representation:", repr(app))
        self.assertEqual(app, Application(f, y))
        self.assertNotEqual(app, Application(f, x))

    # Tests pour le lexer
    def test_lexer(self):
        input_str = "λx.(x y)"
        expected_tokens = [
            Token(Token.LAMBDA),  # λ
            Token(Token.VARIABLE, 'x'),  # x
            Token(Token.DOT),  # .
            Token(Token.LPAREN),  # (
            Token(Token.VARIABLE, 'x'),  # x
            Token(Token.VARIABLE, 'y'),  # y
            Token(Token.RPAREN)  # )
        ]

        tokens = lexer(input_str)
        print("Testing Lexer:")
        print("Expected Tokens:", expected_tokens)
        print("Generated Tokens:", tokens)
        print("equals", tokens == expected_tokens)
        self.assertEqual(tokens, expected_tokens)

    def test_lexer2(self):
        input_str = "λx.λy.x"
        expected_tokens = [
            Token(Token.LAMBDA),  # λ
            Token(Token.VARIABLE, 'x'),  # x
            Token(Token.DOT),  # .
            Token(Token.LAMBDA),  # λ
            Token(Token.VARIABLE, 'y'),  # y
            Token(Token.DOT),  # .
            Token(Token.VARIABLE, 'x')  # x
        ]

        tokens = lexer(input_str)
        print("Testing Lexer2:")
        print("Expected Tokens:", expected_tokens)
        print("Generated Tokens:", tokens)
        print("equals", tokens == expected_tokens)
        self.assertEqual(tokens, expected_tokens)


    # Tests pour le parser
    def test_parser(self):
        input_str = "λx.(x y)"
        tokens = lexer(input_str)
        parser = Parser(tokens)
        parsed_expr = parser.parse()

        # Attendu : une fonction qui prend x et applique x à y
        expected_expr = Function(Variable('x'), Application(Variable('x'), Variable('y')))

        print("Testing Parser:")
        print("Parsed Expression:", parsed_expr)
        self.assertEqual(parsed_expr, expected_expr)

    def test_parser2(self):
        input_str = "λx.λy.x"
        tokens = lexer(input_str)
        parser = Parser(tokens)
        parsed_expr = parser.parse()

        # Attendu : une fonction qui prend x et retourne une fonction qui prend y et retourne x
        expected_expr = Function(Variable('x'), Function(Variable('y'), Variable('x')))

        print("Testing Parser2:")
        print("Parsed Expression:", parsed_expr)
        self.assertEqual(parsed_expr, expected_expr)

    def test_parser3(self):
        input_str = "λx.λy.x y"
        tokens = lexer(input_str)
        parser = Parser(tokens)
        parsed_expr = parser.parse()

        # Attendu : une fonction qui prend x et retourne une fonction qui prend y et applique x à y
        expected_expr = Function(Variable('x'), Function(Variable('y'), Application(Variable('x'), Variable('y'))))

        print("Testing Parser3:")
        print("Parsed Expression:", parsed_expr)
        self.assertEqual(parsed_expr, expected_expr)

    def test_reduce1(self):
        input_str = "λx.(x y)"
        tokens = lexer(input_str)
        parser = Parser(tokens)
        expr = parser.parse()
        evaluator = Evaluator()

        # Attendu : λx.x y
        expected_expr = Function(Variable('x'), Application(Variable('x'), Variable('y')))
        reduced_expr = evaluator.reduce(expr)
        print("Testing Reduce1:")
        print("Reduced Expression:", evaluator.simplify_and_format(reduced_expr))
        self.assertEqual(reduced_expr, expected_expr)


    def test_reduce2(self):
        input_str = "(λx.x) y"
        tokens = lexer(input_str)
        parser = Parser(tokens)
        expr = parser.parse()
        evaluator = Evaluator()

        # Attendu : y
        expected_expr = Variable('y')
        reduced_expr = evaluator.reduce(expr)
        print("Testing Reduce2:")
        print("Reduced Expression:", evaluator.simplify_and_format(expr))
        self.assertEqual(reduced_expr, expected_expr)

    def test_reduce3(self):
        input_str = "(λx.λy.y y) λz.z"
        tokens = lexer(input_str)
        parser = Parser(tokens)
        expr = parser.parse()
        evaluator = Evaluator()

        # Attendu : λy.y y
        expected_expr = Function(Variable('y'), Application(Variable('y'), Variable('y')))
        reduced_expr = evaluator.reduce(expr)
        print("Testing Reduce3:")
        print("Reduced Expression:", evaluator.simplify_and_format(reduced_expr))
        self.assertEqual(reduced_expr, expected_expr)


if __name__ == '__main__':
    unittest.main()
