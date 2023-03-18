from .lexer import Token
from typing import List
from ira.constants import *

binary_operators = {NATURAL_JOIN: TokenType.NATURAL_JOIN, JOIN_LEFT: TokenType.JOIN_LEFT,
                    JOIN_RIGHT: TokenType.JOIN_RIGHT,
                    DIFFERENCE: TokenType.DIFFERENCE, PRODUCT: TokenType.PRODUCT,
                    INTERSECTION: TokenType.INTERSECTION, UNION: TokenType.UNION,
                    DIVISION: TokenType.DIVISION}
unary_operators = {SELECT: TokenType.SELECT, PROJECTION: TokenType.PROJECTION, RENAME: TokenType.RENAME}


class Parser:
    def __init__(self):
        self.precedence = {}
        for op in unary_operators:
            self.precedence[unary_operators[op]] = 2
        for op in binary_operators:
            self.precedence[binary_operators[op]] = 1

    def parse(self, tokens: List[Token]):

        output_queue: List[Token] = []
        operator_stack = []

        for token in tokens:
            if token.type == TokenType.OPEN_PARENTHESIS:
                operator_stack.append(token)
            elif token.type == TokenType.CLOSED_PARENTHESIS:
                while operator_stack[-1].type != TokenType.OPEN_PARENTHESIS:
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()
            elif token.type in self.precedence:
                while operator_stack and operator_stack[-1].type != TokenType.OPEN_PARENTHESIS and \
                        self.precedence[token.type] <= self.precedence[operator_stack[-1].type]:
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)

            else:
                output_queue.append(token)

        while operator_stack:
            output_queue.append(operator_stack.pop())

        return output_queue

    def is_binary_op(self, token: Token):
        return self.precedence[token.type] == 2