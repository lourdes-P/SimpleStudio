from logic.expression_ast.operand_nodes.operand_node import OperandNode

class ParenthesizedExpressionNode(OperandNode):
    
    def __init__(self, sub_expression_node):
        self._sub_expression_node = sub_expression_node

    @property
    def token(self):
        return self._sub_expression_node.token
    
    def is_string(self):
        return self._sub_expression_node.is_string()

    def evaluate(self, processor=None):
        return self._sub_expression_node.evaluate(processor)

    def generate_string(self):
        return f"({self._sub_expression_node.generate_string()})"