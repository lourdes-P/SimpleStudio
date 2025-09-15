
from logic.memories.data_heap_memorycell import DataHeapMemoryCell


class DataCell(DataHeapMemoryCell):
    
    def __init__(self, address=None, annotation=None):
        super().__init__(address, annotation)
        self._actual = False
        self._libre = False
        
    def place_actual(self):
        self._actual = True
        
    def place_libre(self):
        self._libre = True
        
    def remove_actual(self):
        self._actual = False
        
    def remove_libre(self):
        self._libre = False
        
    def generate_register_string(self):
        return "" if self._libre is False and self.actual is False else f"{'Actual' if self._actual else ''}{'&' if self._actual and self._libre else ''}{'Libre' if self._libre else ''} ->"
