from logic.expression_ast.unaryop_nodes.unaryop_node import UnaryOpNode

class NotNode(UnaryOpNode):

    def __init__(self, operator_token, operand_node = None):
        super().__init__(operator_token, operand_node)

    
    def evaluate(self, processor=None):
        operand_evaluation = self._operand_node.evaluate(processor)
        try:
            return int(not int(operand_evaluation))
        except ValueError:
            self._runtime_operand_exception(operand_evaluation, invalid_type_name='string')