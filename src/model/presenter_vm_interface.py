from abc import ABC, abstractmethod
from typing import Optional

class PresenterVMInterface(ABC):
    
    @abstractmethod
    def addListener(self, listener):
        """Add a listener to receive VM notifications."""
        pass
    
    @abstractmethod
    def load_program(self, file_path: str):
        """Load program from the specified file path."""
        pass
    
    @abstractmethod
    def reset(self, on_load: bool = True):
        """Reset the virtual machine to its initial state."""
        pass
    
    @abstractmethod
    def reset_all_time_modified_cells(self):
        """Reset all memory cells that were ever modified during execution."""
        pass
    
    @abstractmethod
    def undo(self):
        """Undo the last executed instruction."""
        pass
    
    @abstractmethod
    def deliver_user_input(self, input: str):
        """Deliver user input to the waiting VM execution engine."""
        pass
    
    @abstractmethod
    def execute_program(self, mode: int, steps: Optional[int] = None):
        """
        Execute the loaded program.
        
        Args:
            mode: Execution mode (COMPLETE, SINGLE_STEP, N_STEP)
            steps: Number of steps for N_STEP mode
        """
        pass
    
    # getters 
    @abstractmethod
    def get_instruction(self, address: int):
        """Get instruction at the specified code memory address."""
        pass
    
    @abstractmethod
    def get_modified_data_cells(self):
        """Get list of modified data memory cells."""
        pass
    
    @abstractmethod
    def get_modified_heap_cells(self):
        """Get list of modified heap memory cells."""
        pass
    
    @abstractmethod
    def get_all_time_modified_data_cells_addresses(self):
        """Get addresses of all data memory cells ever modified."""
        pass
    
    @abstractmethod
    def get_all_time_modified_heap_cells_addresses(self):
        """Get addresses of all heap memory cells ever modified."""
        pass
    
    @abstractmethod
    def get_pc(self) -> int:
        """Get the current PC value."""
        pass
    
    @abstractmethod
    def get_label_address(self, label_name: str):
        """Get the memory address associated with a label."""
        pass
    
    @abstractmethod
    def get_last_triggered_error(self):
        """Get the last error that occurred in the VM."""
        pass
    
    @abstractmethod
    def get_last_executed_instruction_address(self):
        """Get the address of the last executed instruction."""
        pass
    
    @abstractmethod
    def get_user_input(self):
        """Get the last user input provided to the VM."""
        pass
    
    @abstractmethod
    def get_label_dictionary(self):
        """Get the dictionary mapping label names to addresses."""
        pass
    
    @abstractmethod
    def get_last_execution_added_labels(self):
        """Get labels added during the last execution."""
        pass
    
    @abstractmethod
    def get_last_output(self):
        """Get the last output text from the VM."""
        pass
    
    @abstractmethod
    def get_deleted_label_name(self):
        """Get the name of the most recently deleted label."""
        pass
    
    @abstractmethod
    def get_cache_size(self):
        """Get the current size of the undo cache."""
        pass
    
    @abstractmethod
    def get_code_memory(self):
        """Get the code memory structure."""
        pass
    
    @abstractmethod
    def get_data_memory(self):
        """Get the data memory structure."""
        pass
    
    @abstractmethod
    def get_heap_memory(self):
        """Get the heap memory structure."""
        pass
    
    # dependency injection setters
    @abstractmethod
    def set_vm_error_handler(self, error_handler):
        """Set the error handler component."""
        pass
    
    @abstractmethod
    def set_label_manager(self, label_manager):
        """Set the label manager component."""
        pass
    
    @abstractmethod
    def set_memory_manager(self, memory_manager):
        """Set the memory manager component."""
        pass
    
    @abstractmethod
    def set_cache(self, cache):
        """Set the cache component."""
        pass
    
    @abstractmethod
    def set_processor(self, processor):
        """Set the processor component."""
        pass
    
    @abstractmethod
    def set_listeners(self, listeners: list):
        """Set the list of listeners."""
        pass
    
    @abstractmethod
    def set_program_loader(self, program_loader):
        """Set the program loader component."""
        pass
    
    @abstractmethod
    def set_vm_io_handler(self, io_handler):
        """Set the I/O handler component."""
        pass
    
    @abstractmethod
    def set_breakpoint_manager(self, breakpoint_manager):
        """Set the breakpoint manager component."""
        pass
    
    @abstractmethod
    def set_execution_engine(self, execution_engine):
        """Set the execution engine component."""
        pass