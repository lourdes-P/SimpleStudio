class ModifiedCellManager:
    ONLY_REGISTER_MODIFIED = False
    SET_MEMORY_MODIFIED = True
    
    def __init__(self):
        self._modified_data_cells = {}
        self._modified_heap_cells = {}
        self.reset()
    
    def reset(self):
        if self._modified_data_cells.get(self.SET_MEMORY_MODIFIED) is not None:
            self._modified_data_cells[self.SET_MEMORY_MODIFIED].clear()
        else:
            self._modified_data_cells[self.SET_MEMORY_MODIFIED] = []
            
        if self._modified_data_cells.get(self.ONLY_REGISTER_MODIFIED) is not None:
            self._modified_data_cells[self.ONLY_REGISTER_MODIFIED].clear()
        else:
            self._modified_data_cells[self.ONLY_REGISTER_MODIFIED] = []
        
        if self._modified_heap_cells.get(self.SET_MEMORY_MODIFIED) is not None:
            self._modified_heap_cells[self.SET_MEMORY_MODIFIED].clear()
        else:
            self._modified_heap_cells[self.SET_MEMORY_MODIFIED] = []
            
        if self._modified_heap_cells.get(self.ONLY_REGISTER_MODIFIED) is not None:
            self._modified_heap_cells[self.ONLY_REGISTER_MODIFIED].clear()
        else:
            self._modified_heap_cells[self.ONLY_REGISTER_MODIFIED] = []
            
    def add_to_memory_modified_data_cells(self, cell):
        self._add_to_modified_cell_dictionary(self._modified_data_cells, self.SET_MEMORY_MODIFIED, cell)
        
    def add_to_register_modified_data_cells(self, cell):
        self._add_to_modified_cell_dictionary(self._modified_data_cells, self.ONLY_REGISTER_MODIFIED, cell)
        
    def add_to_memory_modified_heap_cells(self, cell):
        self._add_to_modified_cell_dictionary(self._modified_heap_cells, self.SET_MEMORY_MODIFIED, cell)
        
    def add_to_register_modified_heap_cells(self, cell):
        self._add_to_modified_cell_dictionary(self._modified_heap_cells, self.ONLY_REGISTER_MODIFIED, cell)        
              
    def _add_to_modified_cell_dictionary(self, dictionary, key, cell):
        if dictionary.get(key) is not None:
            dictionary[key].append(cell)
            
    def extend_memory_modified_data_cells(self, cell_list):
        self._extend_modified_cell_dictionary_list(self._modified_data_cells, self.SET_MEMORY_MODIFIED, cell_list)
        
    def extend_register_modified_data_cells(self, cell_list):
        self._extend_modified_cell_dictionary_list(self._modified_data_cells, self.ONLY_REGISTER_MODIFIED, cell_list)
        
    def extend_memory_modified_heap_cells(self, cell_list):
        self._extend_modified_cell_dictionary_list(self._modified_heap_cells, self.SET_MEMORY_MODIFIED, cell_list)
        
    def extend_register_modified_heap_cells(self, cell_list):
        self._extend_modified_cell_dictionary_list(self._modified_heap_cells, self.ONLY_REGISTER_MODIFIED, cell_list)
            
    def _extend_modified_cell_dictionary_list(self, dictionary, key, cell_list):
        if dictionary.get(key) is not None:
            dictionary[key].extend(cell_list)
            
    def get_modified_data_cell_dictionary(self):
        return self._modified_data_cells
    
    def get_modified_heap_cell_dictionary(self):
        return self._modified_heap_cells