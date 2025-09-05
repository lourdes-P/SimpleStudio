from abc import ABC, abstractmethod

class VirtualMachineListener(ABC):
    
    @abstractmethod
    def load_has_finished(self):
        pass
    
    @abstractmethod
    def trigger_error(self):
        pass
    
    '''
    @abstractmethod
    def execution_completed(self):
        pass
    
    @abstractmethod
    def partial_execution_completed(self):
        pass
        
        '''