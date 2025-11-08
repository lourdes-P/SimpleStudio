from logic.expression_ast.operand_nodes.operand_node import OperandNode

class StringNode(OperandNode):
    
    def __init__(self, string_token):
        self._token = string_token

    @property
    def token(self):
        return self._token

    def is_string(self):
        return True

    def get_string(self):
        return self._token.lexeme

    def evaluate(self, processor=None):
        return self.get_string()

    def generate_string(self):
        return f"'{self.get_string()}'"