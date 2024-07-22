from token_type import TokenType

class Token:
    def __init__(self, t_type: TokenType, lexeme: str, literal: object, line: int):
        self.t_type = t_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def __str__(self):
        return f"{self.t_type} {self.lexeme} {self.literal}"

    def __repr__(self):
        if self.literal:
            return f"{self.t_type} VAL={self.literal}"
        else:
            return f"{self.t_type}"

