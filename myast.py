import random
import re

class Node:
    def __init__(self):
        pass
    def eval(self):
        return 0

# 数値ノード
class Num(Node):
    def __init__(self, value: int):
        self.value: int = value
        
    def eval(self):
        return self.value
    
    def __str__(self):
        return str(self.value)

# 二項演算ノード
class BinOp(Node):
    def __init__(self, left_child: Node, op: str, right_child: Node):
        self.op: str = op
        self.left_child: Node = left_child
        self.right_child: Node = right_child
        
    def eval(self):
        left: int = self.left_child.eval()
        right: int = self.right_child.eval()
        if self.op == '+':
            return left + right
        elif self.op == '-':
            return left - right
        elif self.op == '*':
            return left * right
        elif self.op == '/':
            return left / right
        elif self.op == 'd':
            total = 0
            for _ in range(int(left)):
                total += random.randint(1, int(right))
            return total
    
    def __str__(self):
        return f"({self.left_child} {self.op} {self.right_child})"

class Tree:
    def __init__(self, root: Node):
        self.root: Node = root
    
    def eval(self):
        return self.root.eval()
    
    def __str__(self):
        return str(self.root)
    
# 字句解析器
# トークンの種類を定義
T_NUM = 'NUM'
T_OP = 'OP'
T_LPAREN = 'LPAREN'
T_RPAREN = 'RPAREN'
T_EOF = 'EOF'
T_SKIP = 'SKIP'
T_MISMATCH = 'MISMATCH'

class Token:
    def __init__(self, type: str, value: str):
        self.type: str = type
        self.value: str = value
        
class Tokenizer:
    def __init__(self, text: str):
        self.text: str = text
        self.pos: int = 0
        self.current_char: str = self.text[self.pos] if self.text else None
        self.token_specification = [
            (T_NUM,      r'\d+(\.\d*)?'),   # Integer or decimal number
            (T_OP,       r'[+\-*/d]'),      # Arithmetic operators
            (T_LPAREN,   r'\('),             # Left Parenthesis
            (T_RPAREN,   r'\)'),             # Right Parenthesis
            (T_SKIP,     r'[ \s]+'),         # Skip over spaces and tabs
            (T_MISMATCH, r'.'),              # Any other character
        ]
        ok_regex: str = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.token_specification)
        self.tok_regex = re.compile(ok_regex)
        
    def tokenize(self):
        tokens = []
        for mo in self.tok_regex.finditer(self.text):
            kind = mo.lastgroup
            value = mo.group()
            if kind == T_NUM:
                tokens.append(Token(T_NUM, value))
            elif kind == T_OP:
                tokens.append(Token(T_OP, value))
            elif kind == T_LPAREN:
                tokens.append(Token(T_LPAREN, value))
            elif kind == T_RPAREN:
                tokens.append(Token(T_RPAREN, value))
            elif kind == T_SKIP:
                continue
            elif kind == T_MISMATCH:
                raise RuntimeError(f"⚠️ `{value} は不正な文字です`")
        tokens.append(Token(T_EOF, None))
        return tokens

# 構文解析器
class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.pos: int = 0
        self.current_token: Token = self.tokens[self.pos]
        
    def _advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(T_EOF, None)
            
    def _eat(self, token_type: str):
        if self.current_token.type == token_type:
            self._advance()
        else:
            raise ValueError(f"⚠️ `不正なトークン: {self.current_token.type}`")
        
    def parse(self) -> Tree:
        node = self._expr()
        if self.current_token.type != T_EOF:
            raise ValueError("⚠️ `不正なトークンが文の最後にあります`")
        return Tree(node)
    
    def _factor(self) -> Node:
        token = self.current_token
        if token.type == T_NUM:
            self._eat(T_NUM)
            return Num(int(token.value))
        elif token.type == T_LPAREN:
            self._eat(T_LPAREN)
            node = self._expr()
            self._eat(T_RPAREN)
            return node
        else:
            raise ValueError(f"⚠️ `不正なトークン: {token.type}`")

    def _term(self) -> Node:
        node = self._factor()
        while self.current_token.type == T_OP and self.current_token.value in ('*', '/', 'd'):
            token = self.current_token
            self._eat(T_OP)
            node = BinOp(left_child=node, op=token.value, right_child=self._factor())
        return node
    
    def _expr(self) -> Node:
        node = self._term()
        while self.current_token.type == T_OP and self.current_token.value in ('+', '-'):
            token = self.current_token
            self._eat(T_OP)
            node = BinOp(left_child=node, op=token.value, right_child=self._term())
        return node