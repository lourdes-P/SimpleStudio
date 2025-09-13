from logic.expression_ast.unaryop_nodes.unaryop_node import UnaryOpNode

class PlusNode(UnaryOpNode):

    def __init__(self, operator_token, operand_node = None):
        super().__init__(operator_token, operand_node)

    
    def evaluate(self, processor=None):
        operand_evaluation = self._operand_node.evaluate(processor)
        return +operand_evaluation