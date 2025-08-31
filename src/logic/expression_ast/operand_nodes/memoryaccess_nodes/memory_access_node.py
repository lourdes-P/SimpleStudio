from logic.expression_ast.operand_nodes.operand_node import OperandNode

class MemoryAccessNode(OperandNode):

    def __init__(self, token, sub_expression_node=None):
        self._token = token
        self._sub_expression_node = sub_expression_node

    def set_sub_expression_node(self, sub_expression_node):
        self._sub_expression_node = sub_expression_node

    def generate_string(self):
        return f"{self._token.lexeme}[{self._sub_expression_node.generate_string()}]"

    def evaluate(self, processor=None):
        pass

    @property
    def token(self):
        return self._token