from abc import ABC
from logic.expression_ast.subexpression_node import SubexpressionNode

class UnaryOpNode(SubexpressionNode, ABC):

    def __init__(self, operator_token, operand_node = None):
        self._operand_node = operand_node
        self._operator_token = operator_token

    def set_operand_node(self, operand_node):
        self._operand_node = operand_node

    @property
    def operand_node(self):
        return self._operand_node
    
    @property
    def token(self):
        return self._operator_token

    def generate_string(self):
        return self._operator_token.lexeme + self._operand_node.generate_string()
