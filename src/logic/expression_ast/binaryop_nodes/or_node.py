from logic.expression_ast.binaryop_nodes.binaryop_node import BinaryOpNode

class OrNode(BinaryOpNode):

    def __init__(self, operator_token, left_side = None, right_side = None):
        super().__init__(operator_token, left_side, right_side)

    def evaluate(self, processor=None):
        pass # TODO