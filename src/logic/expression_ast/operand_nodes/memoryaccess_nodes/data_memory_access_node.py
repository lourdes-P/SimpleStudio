from logic.expression_ast.operand_nodes.memoryaccess_nodes.memory_access_node import MemoryAccessNode

class DataMemoryAccessNode(MemoryAccessNode):

    def __init__(self, token, sub_expression_node=None):
        super().__init__(token, sub_expression_node)

    def evaluate(self, processor=None):
        pass # TODO 
