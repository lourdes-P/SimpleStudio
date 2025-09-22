from abc import ABC, abstractmethod

class DataHeapMemory(ABC):
    
    @abstractmethod
    def initialize_memory(self, cell_number):
        pass
    
    @abstractmethod
    def reset():
        pass
    
    @abstractmethod
    def set_cell(self, address, value = None, annotation = None):
        pass
        
    @abstractmethod
    def get_cell(self, address):
        pass
    
    @property
    @abstractmethod
    def cell_list(self):
        pass
    