
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
        return "" if self._libre is False and self._actual is False else f"{'Act' if self._actual else ''}{'&' if self._actual and self._libre else ''}{'Lib' if self._libre else ''} →"
    
    @property
    def actual(self):
        return self._actual
    
    @property
    def libre(self):
        return self._libre
    
    def clone(self):
        cell = DataCell()
        cell.copy(self)
        
        return cell
    
    def copy(self, data_cell):
        """Copies passed data_cell attribute values into self"""
        super().copy(data_cell)
        if data_cell.actual:
            self.place_actual()
        if data_cell.libre:
            self.place_libre()