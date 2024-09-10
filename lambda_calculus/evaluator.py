from .core import Application, Function, Variable


class Evaluator:
    def reduce(self, expr):
        if isinstance(expr, Application):
            func = self.reduce(expr.func)
            arg = self.reduce(expr.arg)

            if isinstance(func, Function):
                # Réduction bêta : appliquer l'argument à la fonction
                return self.substitute(func.term, func.var, arg)
            else:
                return Application(func, arg)
        elif isinstance(expr, Function):
            # Réduire le corps de la fonction
            return Function(expr.var, self.reduce(expr.term))
        else:
            return expr

    def substitute(self, term, var, value):
        if isinstance(term, Variable):
            return value if term.name == var.name else term
        elif isinstance(term, Function):
            if term.var.name == var.name:
                return term  # Pas de substitution si la variable est la même
            else:
                # Substituer dans le corps de la fonction
                return Function(term.var, self.substitute(term.term, var, value))
        elif isinstance(term, Application):
            # Substituer dans la fonction et l'argument
            return Application(self.substitute(term.func, var, value),
                               self.substitute(term.arg, var, value))
        return term

    def format_expression(self, expr):
        if isinstance(expr, Variable):
            return expr.name
        elif isinstance(expr, Function):
            return f"λ{expr.var.name}.{self.format_expression(expr.term)}"
        elif isinstance(expr, Application):
            func_str = self.format_expression(expr.func)
            arg_str = self.format_expression(expr.arg)
            if isinstance(expr.func, Application):
                func_str = f"({func_str})"
            return f"{func_str} {arg_str}"
        return expr

    def simplify_and_format(self, expr):
        reduced_expr = self.reduce(expr)
        return self.format_expression(reduced_expr)

