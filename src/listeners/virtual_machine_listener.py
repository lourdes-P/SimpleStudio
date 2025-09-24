from abc import ABC, abstractmethod

class VirtualMachineListener(ABC):
    
    @abstractmethod
    def load_has_finished(self):
        pass
    
    @abstractmethod
    def trigger_error(self):
        pass
    
    @abstractmethod
    def trigger_user_input(self):
        pass
    
    @abstractmethod
    def execution_finished(self):
        pass
    
    @abstractmethod
    def reset_has_finished(self):
        pass
    
    @abstractmethod
    def disable_execution(self):
        pass
    
    @abstractmethod
    def enable_execution(self):
        pass
    
    '''
    @abstractmethod
    def execution_completed(self):
        pass
    
    @abstractmethod
    def partial_execution_completed(self):
        pass
        
        '''