from logic.expression_ast.operand_nodes.operand_node import OperandNode

class LibreNode(OperandNode):
    
    def __init__(self, token):
        self._token = token

    @property
    def token(self):
        return self._token

    def evaluate(self, processor=None):
        return int(processor.libre)

    def generate_string(self):
        return str(self.token.lexeme)