from logic.memories.data_heap_memory import DataHeapMemory
from logic.memories.datamemory.datacell import DataCell

class DataMemory(DataHeapMemory):
    
    def __init__(self):
        self._datacell_list = []
        self._actual = 0
        self._libre = 0
        self.initialize_memory(10000)
        
    def initialize_memory(self, cell_number):
        for i in range(cell_number):
            datacell = DataCell(address=i)
            self._datacell_list.append(datacell)
        self._datacell_list[self._actual].place_actual()
        self._datacell_list[self._libre].place_libre()
        
    def place_actual(self, new_address):
        self._datacell_list[self._actual].remove_actual()
        self._actual = new_address
        self._datacell_list[self._actual].place_actual()
        
    def place_libre(self, new_address):
        self._datacell_list[self._libre].remove_libre()
        self._libre = new_address
        self._datacell_list[self._libre].place_libre()
        
    def set_cell(self, address, value = None, annotation = None):
        self._datacell_list[address].set_value(value)
        self._datacell_list[address].set_annotation(annotation)
        
    def get_cell(self, address):
        return self._datacell_list[address]
    
    @property
    def cell_list(self):
        return self._datacell_list
        
    