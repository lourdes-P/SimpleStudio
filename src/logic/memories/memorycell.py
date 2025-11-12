from abc import ABC, abstractmethod

class MemoryCell(ABC):
    
    def __init__(self, address=None, annotation=None):
        self._address = address
        self._annotation = annotation
        
    def set_address(self, address):
        self._address = address
        
    def set_annotation(self, annotation):
        self._annotation = annotation
        
    def annotation_string(self):
        return self._annotation.lexeme if self._annotation != None else ''
    
    @property
    def address(self):
        return self._address
    
    @property
    def annotation(self):
        return self._annotation
    
    @abstractmethod
    def clone(self):
        pass
    
    def copy(self, cell):
        """Copies passed cell attribute values into self"""
        self.set_address(cell.address)
        self.set_annotation(cell.annotation)