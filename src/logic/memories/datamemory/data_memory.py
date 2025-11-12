from logic.memories.data_heap_memory import DataHeapMemory
from logic.memories.datamemory.datacell import DataCell
from logic.memories.exceptions.actual_value_error import ActualValueError
from logic.memories.exceptions.address_out_of_range import MemoryAddressOutOfRangeException
from logic.memories.exceptions.address_value_invalid_exception import AddressValueInvalidException
from logic.memories.exceptions.libre_value_error import LibreValueError

class DataMemory(DataHeapMemory):
    
    def __init__(self, cell_number = 200):
        self._datacell_list = []
        self._actual = 0
        self._libre = 0
        self._initial_cell_number = cell_number
        self._modified = False
        self.initialize_memory(self._initial_cell_number)
        
    def initialize_memory(self, cell_number):
        for i in range(cell_number):
            datacell = DataCell(address=i)
            self._datacell_list.append(datacell)
        self._datacell_list[self._actual].place_actual()
        self._datacell_list[self._libre].place_libre()
    
    def reset(self):
        if self._modified:
            self._actual = 0
            self._libre = 0
            self._datacell_list.clear()
            self.initialize_memory(self._initial_cell_number)
            self._modified = False    
    
    def place_actual(self, new_address):
        try:
            new_address = int(new_address)
            self._modified = True
            self._datacell_list[self._actual].remove_actual()
            self._actual = new_address
            self._datacell_list[self._actual].place_actual()
        except ValueError:
            raise ActualValueError(new_address)
        
    def place_libre(self, new_address):
        try:
            new_address = int(new_address)
            self._modified = True
            self._datacell_list[self._libre].remove_libre()
            self._libre = new_address
            self._datacell_list[self._libre].place_libre()
        except ValueError:
            raise LibreValueError(new_address)
        
    def set_cell(self, address, value = None, annotation = None):
        try:
            if (0 <= int(address) < self._initial_cell_number):
                self._modified = True
                self._datacell_list[address].set_value(value)
                self._datacell_list[address].set_annotation(annotation)
                return self._datacell_list[address]
            else:
                raise MemoryAddressOutOfRangeException(f"Address {address} is out of data memory range.")
        except ValueError:
            raise AddressValueInvalidException(memory_name='data', address_value=address)
        
    def get_cell(self, address):
        try:
            if (0 <= int(address) < self._initial_cell_number):
                return self._datacell_list[address]
            else:
                raise MemoryAddressOutOfRangeException(f"Address {address} is out of data memory range.")
        except ValueError:
            raise AddressValueInvalidException(memory_name='data', address_value=address)
    
    @property
    def cell_list(self):
        return self._datacell_list
        
    