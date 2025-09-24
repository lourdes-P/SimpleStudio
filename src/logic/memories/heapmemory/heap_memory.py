from logic.memories.data_heap_memory import DataHeapMemory
from logic.memories.heapmemory.heapcell import HeapCell

class HeapMemory(DataHeapMemory):
    
    def __init__(self):
        self._heapcell_list = []
        self._po = 0
        self._initial_cell_number = 100
        self.initialize_memory(self._initial_cell_number)
        
    def initialize_memory(self, cell_number):
        for i in range(cell_number):
            heapcell = HeapCell(address=i)
            self._heapcell_list.append(heapcell)
        self._heapcell_list[self._po].place_po()
        
    def reset(self):
        self._po = 0
        self._heapcell_list.clear()
        self.initialize_memory(self._initial_cell_number)
        
    def place_po(self, new_address):
        self._heapcell_list[self._po].remove_po()
        self._po = new_address
        self._heapcell_list[self._po].place_po()
        
    def set_cell(self, address, value = None, annotation = None):
        if (address <= self._initial_cell_number):
            self._heapcell_list[address].set_value(value)
            self._heapcell_list[address].set_annotation(annotation)
            return self._heapcell_list[address]
        else:
            print("ERROR: memory address out of range")
            # TODO excepcion de memoria (out of range)
        
    def get_cell(self, address):
        return self._heapcell_list[address]
    
    @property
    def cell_list(self):
        return self._heapcell_list