from logic.memories.data_heap_memory import DataHeapMemory
from logic.memories.exceptions.address_out_of_range import MemoryAddressOutOfRangeException
from logic.memories.exceptions.address_value_invalid_exception import AddressValueInvalidException
from logic.memories.exceptions.po_value_error import PoValueError
from logic.memories.heapmemory.heapcell import HeapCell

class HeapMemory(DataHeapMemory):
    
    def __init__(self, cell_number = 200):
        self._heapcell_list = []
        self._po = 0
        self._initial_cell_number = cell_number
        self._modified = False
        self.initialize_memory(self._initial_cell_number)
        
    def initialize_memory(self, cell_number):
        for i in range(cell_number):
            heapcell = HeapCell(address=i)
            self._heapcell_list.append(heapcell)
        self._heapcell_list[self._po].place_po()
        
    def reset(self):
        if self._modified:
            self._po = 0
            self._heapcell_list.clear()
            self.initialize_memory(self._initial_cell_number)
            self._modified = False
        
    def place_po(self, new_address):
        try:
            new_address = int(new_address)
            self._modified = True
            self._heapcell_list[self._po].remove_po()
            self._po = new_address
            self._heapcell_list[self._po].place_po()
        except ValueError:
            raise PoValueError(new_address)
        
    def set_cell(self, address, value = None, annotation = None):
        try:
            if (0 <= int(address) < self._initial_cell_number):
                self._modified = True
                self._heapcell_list[address].set_value(value)
                self._heapcell_list[address].set_annotation(annotation)
                return self._heapcell_list[address]
            else:
                raise MemoryAddressOutOfRangeException(f"Address {address} is out of heap memory range")
        except ValueError:
            raise AddressValueInvalidException(memory_name='heap', address_value=address)
        
    def get_cell(self, address):
        try:
            if (0 <= int(address) < self._initial_cell_number):
                return self._heapcell_list[address]
            else:
                raise MemoryAddressOutOfRangeException(f"Address {address} is out of heap memory range")
        except ValueError:
            raise AddressValueInvalidException(memory_name='heap', address_value=address)
    
    @property
    def cell_list(self):
        return self._heapcell_list