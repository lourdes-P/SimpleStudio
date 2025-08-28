from logic.expression_ast.operand_nodes.memoryaccess_nodes.memory_access_node import MemoryAccessNode

class DataMemoryAccessNode(MemoryAccessNode):

    def __init__(self, token, expression_node=None):
        super().__init__(token, expression_node)

    def evaluate(self, processor=None):
        pass # TODO 
