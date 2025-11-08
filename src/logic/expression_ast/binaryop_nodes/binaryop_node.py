from abc import abstractmethod,ABC
from logic.expression_ast.exceptions.invalid_operator_exception import InvalidOperatorException
from logic.expression_ast.subexpression_node import SubexpressionNode

class BinaryOpNode(SubexpressionNode,ABC):

    def __init__(self, operator_token, left_side = None, right_side = None):
        self._operator_token = operator_token
        self._left_side = left_side
        self._right_side = right_side

    def set_left_side(self, left_side):
        self._left_side = left_side
        if self._left_side is not None and self._right_side is not None:
            self._check_sides()

    def set_right_side(self, right_side):
        self._right_side = right_side
        if self._left_side is not None and self._right_side is not None:
            self._check_sides()

    @property
    def left_side(self):
        return self._left_side
    
    @property
    def right_side(self):
        return self._right_side
    
    @property
    def token(self):
        return self._operator_token
    
    @abstractmethod
    def evaluate(self, processor=None):
        pass

    def generate_string(self):
        return self._left_side.generate_string() + self._operator_token.lexeme + self._right_side.generate_string()
    
    def _check_sides(self):
        left_side_contains_string = self.left_side.is_string()
        right_side_contains_string = self.right_side.is_string()
        if left_side_contains_string or right_side_contains_string:
            left_side_class_name = 'string' if left_side_contains_string else 'int'
            right_side_class_name = 'string' if right_side_contains_string else 'int'
            raise InvalidOperatorException(self.token, left_side_class_name, right_side_class_name)