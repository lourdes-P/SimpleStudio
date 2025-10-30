from model.cache.cache_entry import CacheEntry
from model.utils.stack import Stack
from model.exceptions.empty_cache_exception import EmptyCacheException

class Cache:
    
    def __init__(self, capacity):
        self._capacity = capacity
        self._cache_stack = []
        self._last_modified_data_cell_stack = Stack()
        self._last_modified_heap_cell_stack = Stack()
        
    def reset(self):
        self._cache_stack.clear()
        self._last_modified_data_cell_stack.clear()
        self._last_modified_heap_cell_stack.clear()
        
    def create_entry(self, last_executed_instruction_address, pc, memory_modified_data_cell_list = [], register_modified_data_cell_list = [], 
                 memory_modified_heap_cell_list = [], register_modified_heap_cell_list = []):
        entry = CacheEntry(last_executed_instruction_address, pc)
        if memory_modified_data_cell_list is not None:
            entry.set_memory_modified_data_cell_list(memory_modified_data_cell_list)
        if register_modified_data_cell_list is not None:
            entry.set_register_modified_data_cell_list(register_modified_data_cell_list)
        if memory_modified_heap_cell_list is not None:
            entry.set_memory_modified_heap_cell_list(memory_modified_heap_cell_list)
        if register_modified_heap_cell_list is not None:
            entry.set_register_modified_heap_cell_list(register_modified_heap_cell_list)
            
        return entry

    def create_and_push_entry(self, last_executed_instruction_address, pc, memory_modified_data_cell_list = [], register_modified_data_cell_list = [], 
                 memory_modified_heap_cell_list = [], register_modified_heap_cell_list = []):
        self.push(self.create_entry(last_executed_instruction_address, pc, memory_modified_data_cell_list, register_modified_data_cell_list, memory_modified_heap_cell_list, register_modified_heap_cell_list))
        
    def set_last_entry_memory_modified_data_cell_list(self, memory_modified_data_cell_list):
        """Sets last added entry's memory modified data cell list, and appends the overall last modified data cell to the end of the list. 
        It then updates the last modified data cell stack."""
        cloned_cells = self.peek().set_memory_modified_data_cell_list(memory_modified_data_cell_list)
        if self.size() > 1 and self._last_modified_data_cell_stack.size() > 0:
            self.peek().append_memory_modified_data_cell(self._last_modified_data_cell_stack.peek())
        self._last_modified_data_cell_stack.push(cloned_cells[0])
        
    def set_last_entry_memory_modified_heap_cell_list(self, memory_modified_heap_cell_list):
        """Sets last added entry's memory modified heap cell list, and appends the overall last modified heap cell to the end of the list. 
        It then updates the last modified heap cell stack."""
        cloned_cells = self.peek().set_memory_modified_heap_cell_list(memory_modified_heap_cell_list)
        if self.size() > 1 and self._last_modified_heap_cell_stack.size() > 0:
            self.peek().append_memory_modified_heap_cell(self._last_modified_heap_cell_stack.peek())
        self._last_modified_heap_cell_stack.push(cloned_cells[0])
    
    def push(self, entry):
        if self.size() >= self._capacity:
            self._cache_stack.pop(0)
        self._cache_stack.append(entry)
    
    def peek(self):
        if not self.is_empty():
            return self._cache_stack[-1]
        else:
            raise EmptyCacheException()
        
    def pop(self):
        if not self.is_empty():
            entry = self._cache_stack.pop()
            self._pop_last_modified_data_cell_stack(entry.get_memory_modified_data_cells())
            self._pop_last_modified_heap_cell_stack(entry.get_memory_modified_heap_cells())
            return entry
        else:
            raise EmptyCacheException()
    
    def size(self):
        return len(self._cache_stack)
        
    def is_empty(self):
        return len(self._cache_stack) == 0
        
    def _pop_last_modified_data_cell_stack(self, memory_modified_data_cell_list):
        last_modified = self._last_modified_data_cell_stack.peek()
        if memory_modified_data_cell_list is not None and len(memory_modified_data_cell_list) > 0 and memory_modified_data_cell_list[0] == last_modified:
            self._last_modified_data_cell_stack.pop()
    
    def _pop_last_modified_heap_cell_stack(self, memory_modified_heap_cell_list):
        last_modified = self._last_modified_heap_cell_stack.peek()
        if memory_modified_heap_cell_list is not None and len(memory_modified_heap_cell_list) > 0 and memory_modified_heap_cell_list[0] == last_modified:
            self._last_modified_heap_cell_stack.pop()