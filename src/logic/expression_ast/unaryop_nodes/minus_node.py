from logic.expression_ast.unaryop_nodes.unaryop_node import UnaryOpNode

class MinusNode(UnaryOpNode):

    def __init__(self, operator_token, operand_node = None):
        super().__init__(operator_token, operand_node)

    
    def evaluate(self, processor=None):
        pass