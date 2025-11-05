from logic.expression_ast.binaryop_nodes.binaryop_node import BinaryOpNode

class LesserOrEqualNode(BinaryOpNode):

    def __init__(self, operator_token, left_side = None, right_side = None):
        super().__init__(operator_token, left_side, right_side)

    def evaluate(self, processor=None):
        left_side_evaluation = self.left_side.evaluate(processor)
        right_side_evaluation = self.right_side.evaluate(processor)
        return int(int(left_side_evaluation) <= int(right_side_evaluation))