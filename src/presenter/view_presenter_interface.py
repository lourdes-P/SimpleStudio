from abc import ABC, abstractmethod

class ViewPresenterInterface(ABC):
    
    @abstractmethod
    def on_file_selected(self):
        pass
    
    @abstractmethod
    def on_user_input(self):
        pass
    
    @abstractmethod
    def on_breakpoint_change(self):
        pass
    
    @abstractmethod
    def on_complete_execution(self):
        pass
    
    @abstractmethod
    def on_single_step_execution(self):
        pass
    
    @abstractmethod
    def on_undo(self):
        pass
    
    @abstractmethod
    def on_save_file(self):
        pass