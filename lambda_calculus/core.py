class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __call__(self, *args):
        return self

    def substitute(self, var, term):
        return term if self == var else self

    def free_variables(self):
        return {self}


class Function:
    def __init__(self, var, term):
        self.var = var
        self.term = term

    def __str__(self):
        return f'λ{self.var}.{self.term}'

    def __repr__(self):
        return f'Function({self.var}, {self.term})'

    def __eq__(self, other):
        return isinstance(other, Function) and self.var == other.var and self.term == other.term

    def __hash__(self):
        return hash((self.var, self.term))

    def alpha_convert(self, new_var):
        if new_var in self.term.free_variables():
            new_name = self.generate_unique_var_name(self.var)
            new_term = self.term.substitute(self.var, Variable(new_name))
            return Function(Variable(new_name), new_term)
        return self

    def generate_unique_var_name(self, var):
        return Variable(var.name + "'")

    def substitute(self, var, term):
        if self.var == var:
            return self
        else:
            return Function(self.var, self.term.substitute(var, term))


class Application:
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg

    def __str__(self):
        func_str = f'({self.func})' if isinstance(self.func, Application) else str(self.func)
        return f'{self.func} {self.arg}'

    def __repr__(self):
        return f'Application({self.func}, {self.arg})'

    def __eq__(self, other):
        return isinstance(other, Application) and self.func == other.func and self.arg == other.arg

    def __hash__(self):
        return hash((self.func, self.arg))

