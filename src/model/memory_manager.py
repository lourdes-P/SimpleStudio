from model.cache.cache import Cache
from model.cache.cache_entry import CacheEntry
from model.utils.modified_cell_manager import ModifiedCellManager
from logic.memories.datamemory.data_memory import DataMemory
from logic.memories.heapmemory.heap_memory import HeapMemory
from logic.memories.codememory.codememory import CodeMemory

class MemoryManager:
    
    def __init__(self):
        self._code_memory = None
        self._data_memory = DataMemory(1000)
        self._heap_memory = HeapMemory(1000)
        self._modified_cell_manager = ModifiedCellManager()
        self._all_time_modified_data_cells_addresses = []
        self._all_time_modified_heap_cells_addresses = []
        
    def reset(self, only_modified_cells = False):
        if not only_modified_cells:
            self._data_memory.reset()
            self._heap_memory.reset()
        self._modified_cell_manager.reset()
    
    def reset_all_time_modified_cells(self):
        self._all_time_modified_data_cells_addresses.clear()
        self._all_time_modified_heap_cells_addresses.clear()
    
    def set_data_memory(self, cache: Cache, address, data = None, source_instruction_address = None):
        annotation = None
        if source_instruction_address is not None:
            annotation = self._code_memory.get_codecell(source_instruction_address).annotation
        cell = self._data_memory.get_cell(address)
        cache.set_last_entry_memory_modified_data_cell_list([cell])
        modified_cell = self._data_memory.set_cell(address, data, annotation)
        self._modified_cell_manager.add_to_memory_modified_data_cells(modified_cell)
        self._all_time_modified_data_cells_addresses.append(address)
    
    def set_heap_memory(self, cache: Cache, address, data = None, source_instruction_address = None):
        annotation = None
        if source_instruction_address is not None:
            annotation = self._code_memory.get_codecell(source_instruction_address).annotation
        cell = self._heap_memory.get_cell(address)
        cache.set_last_entry_memory_modified_heap_cell_list([cell])
        modified_cell = self._heap_memory.set_cell(address, data, annotation)
        self._modified_cell_manager.add_to_memory_modified_heap_cells(modified_cell)
        self._all_time_modified_heap_cells_addresses.append(address)
        
    def set_libre(self, cache_entry: CacheEntry, former_libre, libre):
        former = self._data_memory.get_cell(former_libre)
        new = self._data_memory.get_cell(libre)
        cache_entry.set_register_modified_data_cell_list([new, former])
        self._data_memory.place_libre(libre)
        self._modified_cell_manager.add_to_register_modified_data_cells(former)
        self._modified_cell_manager.add_to_register_modified_data_cells(new)
        self._all_time_modified_data_cells_addresses.append(new.address)
        self._all_time_modified_data_cells_addresses.append(former.address)
        
    def set_actual(self, cache_entry: CacheEntry, former_actual, actual):
        former = self._data_memory.get_cell(former_actual)
        new = self._data_memory.get_cell(actual)
        cache_entry.set_register_modified_data_cell_list([new, former])
        self._data_memory.place_actual(actual)
        self._modified_cell_manager.add_to_register_modified_data_cells(former)
        self._modified_cell_manager.add_to_register_modified_data_cells(new)
        self._all_time_modified_data_cells_addresses.append(new.address)
        self._all_time_modified_data_cells_addresses.append(former.address) 
        
    def set_po(self, cache_entry: CacheEntry, former_po, po):
        former = self._heap_memory.get_cell(former_po)
        new = self._heap_memory.get_cell(po)
        cache_entry.set_register_modified_heap_cell_list([new, former])
        self._heap_memory.place_po(po)
        self._modified_cell_manager.add_to_register_modified_heap_cells(former)
        self._modified_cell_manager.add_to_register_modified_heap_cells(new)
        self._all_time_modified_heap_cells_addresses.append(new.address)
        self._all_time_modified_heap_cells_addresses.append(former.address)
      
    def access_data_memory(self, address):
        value = self._data_memory.get_cell(address).value
        return value
    
    def access_heap_memory(self, address):
        value = self._heap_memory.get_cell(address).value
        return value
      
    def get_code_memory(self, new_memory = False):
        if new_memory:
            self._code_memory = CodeMemory()
        return self._code_memory
    
    def there_is_code_memory(self):
        return self._code_memory is not None and not self._code_memory.is_empty()
    
    def get_data_memory(self):
        return self._data_memory
    
    def get_heap_memory(self):
        return self._heap_memory
    
    def get_instruction(self, address):
        return self._code_memory.get_instruction(address)
    
    def get_all_time_modified_data_cells_addresses(self):
        return self._all_time_modified_data_cells_addresses.copy() 
    
    def get_all_time_modified_heap_cells_addresses(self):
        return self._all_time_modified_heap_cells_addresses.copy()
    
    def get_modified_data_cells(self):
        return self._modified_cell_manager.get_modified_data_cell_dictionary()
    
    def get_modified_heap_cells(self):
        return self._modified_cell_manager.get_modified_heap_cell_dictionary()
    
    # UNDO methods
    
    def undo_memory_modified_data_cells(self, memory_modified_data_cells):
        original_data_cells = []
        modified_cells_size = len(memory_modified_data_cells)
        if modified_cells_size > 0:
            if modified_cells_size == 1:
                original_data_cells.append(self._undo_datacell(memory_modified_data_cells[0]))
            else:
                last_modified_cell = memory_modified_data_cells[-1]
                for i in range(0,modified_cells_size-1):
                    original_data_cells.append(self._undo_datacell(memory_modified_data_cells[i]))
                original_data_cells.append(self._data_memory.get_cell(last_modified_cell.address))
            self._modified_cell_manager.extend_memory_modified_data_cells(original_data_cells)
    
    def _undo_datacell(self, data_cell_clone):
        address = data_cell_clone.address
        return self._data_memory.set_cell(address, data_cell_clone.value, data_cell_clone.annotation)
            
    def undo_register_modified_data_cells(self, processor, register_modified_data_cells):
        for undo_modified_cell in register_modified_data_cells:
            address = undo_modified_cell.address
            if undo_modified_cell.libre:
                processor.reinstate_libre(address)
                self._data_memory.place_libre(address)
            if undo_modified_cell.actual:
                processor.reinstate_actual(address)
                self._data_memory.place_actual(address)
        
        self._modified_cell_manager.extend_register_modified_data_cells(register_modified_data_cells)
    
    def undo_memory_modified_heap_cells(self, memory_modified_heap_cells):
        original_heap_cells = []
        modified_cells_size = len(memory_modified_heap_cells)
        if modified_cells_size > 0:
            if modified_cells_size == 1:
                original_heap_cells.append(self._undo_heapcell(memory_modified_heap_cells[0]))
            else:
                last_modified_cell = memory_modified_heap_cells[-1]
                for i in range(0,modified_cells_size-1):
                    original_heap_cells.append(self._undo_heapcell(memory_modified_heap_cells[i]))
                original_heap_cells.append(self._heap_memory.get_cell(last_modified_cell.address))
            self._modified_cell_manager.extend_memory_modified_heap_cells(original_heap_cells)
    
    def _undo_heapcell(self, heap_cell_clone):
        address = heap_cell_clone.address
        return self._heap_memory.set_cell(address, heap_cell_clone.value, heap_cell_clone.annotation)
         
    def undo_register_modified_heap_cells(self, processor, register_modified_heap_cells):
        for undo_modified_cell in register_modified_heap_cells:
            address = undo_modified_cell.address
 
            if undo_modified_cell.po:
                processor.reinstate_po(address)
                self._heap_memory.place_po(address)
        
        self._modified_cell_manager.extend_register_modified_heap_cells(register_modified_heap_cells)