from logic.expression_ast.binaryop_nodes.binaryop_node import BinaryOpNode

class AndNode(BinaryOpNode):

    def __init__(self, operator_token, left_side = None, right_side = None):
        super().__init__(operator_token, left_side, right_side)

    def evaluate(self, processor=None):
        left_side_evaluation = self.left_side.evaluate(processor)
        right_side_evaluation = self.right_side.evaluate(processor)
        try:
            return int(int(left_side_evaluation) and int(right_side_evaluation))
        except ValueError:
            self._runtime_operand_exception(left_side_evaluation, right_side_evaluation, invalid_type_name='string')