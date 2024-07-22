from typing import List
from lox_token import Token
from token_type import TokenType
from lox import Lox

class Scanner:
    
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> List[str]:
        while(not self.is_at_end()):
            self.start = self.current
            self.scan_token()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return list()
    
    def scan_token(self) -> None:
        c = self.advance()
        if c == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == '.':
            self.add_token(TokenType.DOT)
        elif c == '-':
            self.add_token(TokenType.MINUS)
        elif c == '+':
            self.add_token(TokenType.PLUS)
        elif c == ';':
            self.add_token(TokenType.SEMICOLON)
        elif c == '*':
            self.add_token(TokenType.STAR)
        elif c == '!':
            self.add_token(
                TokenType.BANG_EQUAL if self.match('=') 
                else TokenType.BANG
            )
        elif c == '<':
            self.add_token(
                TokenType.LESS_EQUAL if self.match('=') 
                else TokenType.LESS
            )
        elif c == '>':
            self.add_token(
                TokenType.GREATER_EQUAL if self.match('=') 
                else TokenType.GREATER
            )
        elif c == '=':
            self.add_token(
                TokenType.EQUAL_EQUAL if self.match('=') 
                else TokenType.EQUAL
            )
        else:
            Lox.error(self.line, "Unexpected character.")
            
    def add_token(self,token_type: TokenType, literal: object = None) -> None:
        text = self.source[self.start:self.current]
        token = Token(token_type, text, literal, self.line)
        self.tokens.append(token_type)
        print(self.tokens)


    def advance(self) -> str:
        assert self.current < len(self.source), "Reached end of source."
        current_char = self.source[self.current]
        self.current += 1
        return current_char

    def match(self, excepted: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != excepted:
            return False
        
        self.current += 1
        return True

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
        