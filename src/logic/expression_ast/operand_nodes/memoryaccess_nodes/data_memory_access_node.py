from logic.expression_ast.operand_nodes.memoryaccess_nodes.memory_access_node import MemoryAccessNode
from logic.expression_ast.exceptions.datacell_value_notset_exception import DatacellValueNotSetException

class DataMemoryAccessNode(MemoryAccessNode):

    def __init__(self, token, sub_expression_node=None):
        super().__init__(token, sub_expression_node)

    def evaluate(self, processor=None):
        address = self._sub_expression_node.evaluate(processor)
        value = processor.access_data_memory(address)
        if value is not None:
            return value
        else:
            raise DatacellValueNotSetException(address)