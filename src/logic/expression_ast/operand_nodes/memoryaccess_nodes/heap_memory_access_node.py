from logic.expression_ast.operand_nodes.memoryaccess_nodes.memory_access_node import MemoryAccessNode
from logic.expression_ast.exceptions.heapcell_value_notset_exception import HeapcellValueNotSetException

class HeapMemoryAccessNode(MemoryAccessNode):

    def __init__(self, token, sub_expression_node=None):
        super().__init__(token, sub_expression_node)

    def evaluate(self, processor=None):
        address = self._sub_expression_node.evaluate(processor)
        value = processor.access_heap_memory(address)
        if value is not None:
            return value
        else:
            raise HeapcellValueNotSetException(address)