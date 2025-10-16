from abc import ABC, abstractmethod
from logic.memories.memorycell import MemoryCell

class DataHeapMemoryCell(MemoryCell, ABC):
    
    def __init__(self, address=None, annotation=None):
        super().__init__(address, annotation)
        self._value = None
        
    def set_value(self, value):
        self._value = value
        
    def remove_value(self):
        self._value = None
        
    @property
    def value(self):
        return self._value
        
    @abstractmethod
    def generate_register_string(self):
        pass
        
    def copy(self, data_heap_cell):
        """Copies passed cell attribute values into self"""
        super().copy(data_heap_cell)
        self.set_value(data_heap_cell.value)