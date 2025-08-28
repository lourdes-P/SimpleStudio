from logic.expression_ast.operand_nodes.operand_node import OperandNode

class ParenthesizedExpressionNode(OperandNode):
    
    def __init__(self, expression_node):
        self._expression_node = expression_node

    @property
    def token(self):
        return self._expression_node.subexpression_node.token
    # TODO ver cómo se comporta binarios y accesos

    def evaluate(self, processor=None):
        pass # TODO

    def generate_string(self):
        return f"({self._expression_node.generate_string()})"