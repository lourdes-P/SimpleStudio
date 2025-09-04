from logic.expression_ast.operand_nodes.operand_node import OperandNode

class StringNode(OperandNode):
    
    def __init__(self, string_token):
        self._token = string_token

    @property
    def token(self):
        return self._token

    def get_string(self):
        return self._token.lexeme

    def evaluate(self, processor=None):
        pass # TODO

    def generate_string(self):
        return self.get_string()