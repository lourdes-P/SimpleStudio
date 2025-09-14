from logic.expression_ast.operand_nodes.operand_node import OperandNode

# registro Actual
class ActualNode(OperandNode):
    
    def __init__(self, token):
        self._token = token

    @property
    def token(self):
        return self._token

    def evaluate(self, processor=None):
        return processor.actual()

    def generate_string(self):
        return str(self.token.lexeme)