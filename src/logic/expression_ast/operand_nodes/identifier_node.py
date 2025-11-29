from logic.expression_ast.operand_nodes.operand_node import OperandNode

class IdentifierNode(OperandNode):
    
    def __init__(self, identifier):
        self._token = identifier

    @property
    def token(self):
        return self._token
    
    def get_name(self):
        return self._token.lexeme

    def evaluate(self, processor=None):
        return processor.get_label_address(self.get_name())

    def generate_string(self):
        return str(self.get_name())