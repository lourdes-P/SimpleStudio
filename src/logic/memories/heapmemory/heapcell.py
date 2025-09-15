from logic.memories.data_heap_memorycell import DataHeapMemoryCell

class HeapCell(DataHeapMemoryCell):
    
    def __init__(self, address=None, annotation=None):
        super().__init__(address, annotation)
        self._po = False
        
    def place_po(self):
        self._po = True
        
    def remove_po(self):
        self._po = False
        
    def generate_register_string(self):
        return "" if self._po is False else f"{'PO' if self._actual else ''} ->"