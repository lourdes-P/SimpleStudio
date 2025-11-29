from abc import ABC, abstractmethod

class ProcessorVMInterface(ABC):
    
    @abstractmethod
    def access_data_memory(self, address: int):
        """Access data memory at the specified address."""
        pass
    
    @abstractmethod
    def access_heap_memory(self, address: int):
        """Access heap memory at the specified address."""
        pass
    
    @abstractmethod
    def set_data_memory(self, address: int, data = None, 
                       source_instruction_address = None):
        """Set data memory at the specified address. source_instruction_address purpose is to get corresponding instruction annotation from code memory."""
        pass
    
    @abstractmethod
    def set_heap_memory(self, address: int, data = None,
                       source_instruction_address = None):
        """Set heap memory at the specified address. source_instruction_address purpose is to get corresponding instruction annotation from code memory."""
        pass
    
    @abstractmethod
    def set_libre(self, former_libre, libre):
        """Set the libre pointer."""
        pass
    
    @abstractmethod
    def set_actual(self, former_actual, actual):
        """Set the actual pointer."""
        pass
    
    @abstractmethod
    def set_po(self, former_po, po):
        """Set the po pointer."""
        pass
    
    @abstractmethod
    def define_label(self, label_token: str, address: int):
        """
        Define a label at the specified address.
        
        Returns:
            Processor.SUCCESS or Processor.FAILURE
        """
        pass