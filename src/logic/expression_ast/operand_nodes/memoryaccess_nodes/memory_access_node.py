from logic.expression_ast.exceptions.invalid_memory_access_operand_exception import InvalidMemoryAccessOperandException
from logic.expression_ast.operand_nodes.operand_node import OperandNode

class MemoryAccessNode(OperandNode):

    def __init__(self, token, sub_expression_node=None):
        self._token = token
        self._sub_expression_node = sub_expression_node
        self._check_subexpression_node()

    def set_sub_expression_node(self, sub_expression_node):
        self._sub_expression_node = sub_expression_node
        self._check_subexpression_node()

    def generate_string(self):
        return f"{self._token.lexeme}[{self._sub_expression_node.generate_string()}]"

    def evaluate(self, processor=None):
        pass
    
    def _check_subexpression_node(self):
        if self._sub_expression_node is not None and self._sub_expression_node.is_string():
            raise InvalidMemoryAccessOperandException(self._token, self, 'string')

    @property
    def token(self):
        return self._token