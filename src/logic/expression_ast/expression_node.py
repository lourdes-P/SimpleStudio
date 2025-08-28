class ExpressionNode:

    def __init__(self, subexpression_node = None):
        self._subexpression_node = subexpression_node
        #self._has_right_side_expression = has_right_side_expression

    def set_subexpression_node(self, subexpression_node):
        self._subexpression_node = subexpression_node
        #self._has_right_side_expression = has_right_side_expression

    """@property
    def has_right_side_expression(self):
        return self._has_right_side_expression"""
    
    @property
    def subexpression_node(self):
        return self._subexpression_node
    
    def evaluate(self, processor):
        pass # TODO ver cómo evaluar los nodos de AST
    
    def generate_string(self):
        self._subexpression_node.generate_string()
