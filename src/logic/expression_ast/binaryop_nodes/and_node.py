from logic.expression_ast.binaryop_nodes.binaryop_node import BinaryOpNode
from logic.expression_ast.exceptions.invalid_operator_exception import InvalidOperatorException

class AndNode(BinaryOpNode):

    def __init__(self, operator_token, left_side = None, right_side = None):
        super().__init__(operator_token, left_side, right_side)

    def evaluate(self, processor=None):
        left_side_evaluation = self.left_side.evaluate(processor)
        right_side_evaluation = self.right_side.evaluate(processor)
        return int(left_side_evaluation and right_side_evaluation)
    
    def _check_sides(self):
        # String s = (("hola").equals("hola")) &&  true  + "string";
        left_side_contains_string = self.left_side.contains_string()
        right_side_contains_string = self.right_side.contains_string()
        if left_side_contains_string or right_side_contains_string:
            left_side_class_name = 'string' if left_side_contains_string else 'int'
            right_side_class_name = 'string' if right_side_contains_string else 'int'
            raise InvalidOperatorException(self.token, left_side_class_name, right_side_class_name)