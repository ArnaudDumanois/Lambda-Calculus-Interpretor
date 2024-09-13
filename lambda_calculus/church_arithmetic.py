from .core import Application, Function, Variable

def church_numeral(n):
    """Return the Church numeral for n."""
    if n == 0:
        return Function(Variable('f'), Function(Variable('x'), Variable('x')))
    else:
        body = Variable('x')
        for _ in range(n):
            body = Application(Variable('f'), body)
        return Function(Variable('f'), Function(Variable('x'), body))

def church_add(m, n):
    """Return the Church numeral for m + n."""
    return Function(Variable('f'), Function(Variable('x'),
                        Application(
                            Application(m, Variable('f')),
                            Application(
                                Application(n, Variable('f')),
                                Variable('x')
                            )
                        )))

def church_multiply(m, n):
    """Return the Church numeral for m * n."""
    return Function(Variable('f'), Function(Variable('x'),
                        Application(
                            Application(m, Application(n, Variable('f'))),
                            Variable('x')
                        )))
