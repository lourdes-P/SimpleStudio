
from model.utils.cache_parser import CacheParser


class CacheEntry:
    
    def __init__(self, last_executed_instruction_address, pc, memory_modified_data_cell_list = [], register_modified_data_cell_list = [], 
                 memory_modified_heap_cell_list = [], register_modified_heap_cell_list = [], label_added_entry = None): 
        self._last_executed_instruction_address = last_executed_instruction_address
        self._pc = pc
        self._memory_modified_data_cell_list = CacheParser.clone_cell_list(memory_modified_data_cell_list)
        self._register_modified_data_cell_list = CacheParser.clone_cell_list(register_modified_data_cell_list)
        self._memory_modified_heap_cell_list = CacheParser.clone_cell_list(memory_modified_heap_cell_list)
        self._register_modified_heap_cell_list = CacheParser.clone_cell_list(register_modified_heap_cell_list)
        self._label_added_entry = label_added_entry
        
    def set_last_executed_instruction_address(self, last_executed_instruction_address):
        self._last_executed_instruction_address = last_executed_instruction_address
        
    def set_pc(self, pc):
        self._pc = pc

    def set_memory_modified_data_cell_list(self, memory_modified_data_cell_list):
        """Clone all cells in list and set"""
        self._memory_modified_data_cell_list = CacheParser.clone_cell_list(memory_modified_data_cell_list)
        return self._memory_modified_data_cell_list
    
    def set_register_modified_data_cell_list(self, register_modified_data_cell_list):
        """Clone all cells in list and set"""
        self._register_modified_data_cell_list = CacheParser.clone_cell_list(register_modified_data_cell_list)
    
    def set_memory_modified_heap_cell_list(self, memory_modified_heap_cell_list):
        """Clone all cells in list and set"""
        self._memory_modified_heap_cell_list = CacheParser.clone_cell_list(memory_modified_heap_cell_list)
        return self._memory_modified_heap_cell_list
    
    def set_register_modified_heap_cell_list(self, register_modified_heap_cell_list):
        """Clone all cells in list and set"""
        self._register_modified_heap_cell_list = CacheParser.clone_cell_list(register_modified_heap_cell_list)
        
    def set_label_added_entry(self, label_added_entry):
        """
        Args:
            label_added_entry: dictionary with format { label_name (lowercase)  former_address }
        """
        self._label_added_entry = label_added_entry
        
    def append_memory_modified_data_cell(self, memory_modified_data_cell):
        """Appends same cell from args to memory modified data cell list."""
        self._memory_modified_data_cell_list.append(memory_modified_data_cell)
        
    def append_memory_modified_heap_cell(self, memory_modified_heap_cell):
        """Appends same cell from args to memory modified heap cell list."""
        self._memory_modified_heap_cell_list.append(memory_modified_heap_cell)
    
    def get_last_executed_instruction_address(self):
        return self._last_executed_instruction_address
        
    def get_pc(self):
        return self._pc
    
    def get_memory_modified_data_cells(self):
        return self._memory_modified_data_cell_list
    
    def get_register_modified_data_cells(self):
        return self._register_modified_data_cell_list
    
    def get_memory_modified_heap_cells(self):
        return self._memory_modified_heap_cell_list
    
    def get_register_modified_heap_cells(self):
        return self._register_modified_heap_cell_list
    
    def get_label_added_entry(self):
        """Returns label name with former corresponding address as a dictionary:
        { label_name (lowercase) : former_address }.
        If former_address is None, it is expected for the label of name label_name to be deleted."""
        return self._label_added_entry