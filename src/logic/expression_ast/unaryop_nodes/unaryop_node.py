from abc import ABC
from logic.expression_ast.exceptions.runtime_invalid_operand_exception import RuntimeInvalidOperandException
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
    
    def _runtime_operand_exception(self, evaluation, invalid_type_name):
        class_name = self._get_type(evaluation)

        if class_name == invalid_type_name:
            raise RuntimeInvalidOperandException(self._operator_token, invalid_type_name, evaluation)