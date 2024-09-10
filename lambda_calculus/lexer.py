import re

# Classe Token pour représenter les différents types de tokens
class Token:
    VARIABLE = 'VARIABLE'
    LAMBDA = 'LAMBDA'
    DOT = 'DOT'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'

    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'

    def __eq__(self, other):
        return isinstance(other, Token) and self.type == other.type and self.value == other.value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

    def __hash__(self):
        return hash((self.type, self.value))


# Fonction pour tokenizer une chaîne de caractères en tokens
def lexer(input_str):
    tokens = []
    pos = 0
    while pos < len(input_str):
        char = input_str[pos]
        if char.isspace():
            pos += 1
            continue
        elif char == 'λ':
            tokens.append(Token(Token.LAMBDA))
        elif char == '.':
            tokens.append(Token(Token.DOT))
        elif char == '(':
            tokens.append(Token(Token.LPAREN))
        elif char == ')':
            tokens.append(Token(Token.RPAREN))
        elif re.match(r'[a-z]', char):  # Variable
            tokens.append(Token(Token.VARIABLE, char))
        else:
            raise SyntaxError(f"Invalid character: {char}")
        pos += 1
    return tokens
