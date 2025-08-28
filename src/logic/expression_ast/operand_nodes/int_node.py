from logic.expression_ast.operand_nodes.operand_node import OperandNode

class IntNode(OperandNode):
    
    def __init__(self, int_token):
        self._token = int_token

    @property
    def token(self):
        return self._token
    # TODO ver cómo se comporta binarios y accesos

    def get_int(self):
        return self._token.lexeme

    def evaluate(self, processor=None):
        pass # TODO

    def generate_string(self):
        return str(self.get_int())