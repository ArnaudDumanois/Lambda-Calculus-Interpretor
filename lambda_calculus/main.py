from lambda_calculus.core import Variable, Function, Application
from lambda_calculus.lexer import lexer
from lambda_calculus.parser import Parser
from lambda_calculus.evaluator import Evaluator

def main():
    expr = Application(
        Function(Variable('x'), Function(Variable('y'), Application(Variable('y'), Variable('y')))),
        Variable('z')
    )

    evaluator = Evaluator()
    print("Expression:", evaluator.simplify_and_format(expr))

    input_str = "(λx.λy.y y) λz.z"
    tokens = lexer(input_str)
    print("Tokens:", tokens)
    parser = Parser(tokens)
    expr = parser.parse()
    print("Expression:", expr)
    print("Expression:", parser.print_expression(expr))
    evaluator = Evaluator()
    reduced_expr = evaluator.reduce(expr)
    print("Reduced Expression:", evaluator.simplify_and_format(reduced_expr))


if __name__ == '__main__':
    main()