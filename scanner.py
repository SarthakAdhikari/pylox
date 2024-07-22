from typing import List
from lox_token import Token
from token_type import TokenType
from lox import Lox

keywords = {
    "and":    TokenType.AND,
    "class":  TokenType.CLASS,
    "else":   TokenType.ELSE,
    "false":  TokenType.FALSE,
    "for":    TokenType.FOR,
    "fun":    TokenType.FUN,
    "if":     TokenType.IF,
    "nil":    TokenType.NIL,
    "or":     TokenType.OR,
    "print":  TokenType.PRINT,
    "return": TokenType.RETURN,
    "super":  TokenType.SUPER,
    "this":   TokenType.THIS,
    "true":   TokenType.TRUE,
    "var":    TokenType.VAR,
    "while":  TokenType.WHILE,
}

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
        
        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
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
        elif c == '/':
            # comments also start with / so handle them
            if self.match('/'):
                while(self.peek() != '\n' and not self.is_at_end()):
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c in [' ', '\r','\t']:
            pass
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.string()
        else:
            if c.isdigit():
                self.number()
            elif c.isalpha():
                self.identifier()
            else:
                Lox.error(self.line, 'Unexpected character.')
            
    def add_token(self,token_type: TokenType, literal: object = None) -> None:
        text = self.source[self.start:self.current]
        token = Token(token_type, text, literal, self.line)
        self.tokens.append(token)
        print(self.tokens)


    def advance(self) -> str:
        assert self.current < len(self.source), 'Reached end of source.'
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
    
    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]
    
        
    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current+1]
    
    def string(self) -> None:
        while(self.peek() != '"' and not self.is_at_end()):
            if (self.peek() == "\n"):
                self.line += 1
            self.advance()
        
        if (self.is_at_end()):
            Lox.error(self.line, "Unterminated string.")
            return
        
        self.advance()

        val: str = self.source[self.start+1:self.current - 1]
        self.add_token(TokenType.STRING, val)
    
    def identifier(self) -> None:
        while(self.peek().isalnum()):
            self.advance()
        text: str = self.source[self.start:self.current]
        token_type = keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    def number(self) -> str:
        while(self.peek().isdigit()):
            self.advance()
        
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            
            while(self.peek().isdigit()):
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))
    
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
        