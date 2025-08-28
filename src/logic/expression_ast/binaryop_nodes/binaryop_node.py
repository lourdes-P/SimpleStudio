from logic.expression_ast.subexpression_node import SubexpressionNode

class BinaryOpNode(SubexpressionNode):

    def __init__(self, operator_token, left_side = None, right_side = None):
        self._operator_token = operator_token
        self._left_side = left_side
        self._right_side = right_side

    def set_left_side(self, left_side):
        self._left_side = left_side

    def set_right_side(self, right_side):
        self._right_side = right_side

    @property
    def left_side(self):
        return self._left_side
    
    @property
    def right_side(self):
        return self._right_side
    
    @property
    def token(self):
        return self._operator_token
    
    def evaluate(self, processor=None):
        pass    #   TODO

    def generate_string(self):
        return self._left_side.generate_string() + self._operator_token.lexeme + self._right_side.generate_string()