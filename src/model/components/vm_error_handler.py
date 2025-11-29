
class VMErrorHandler:
    
    def __init__(self, virtual_machine=None):
        self._virtual_machine = virtual_machine
        self._error = None
    
    def reset(self):
        self._error = None
        
    def register_error(self, error):
        self._error = error
        self._virtual_machine.notify_error()
        
    def set_error(self, error):
        self._error = error
                
    def error_registered(self):
        return self._error is not None
    
    def get_last_registered_error(self):
        return self._error
    
    def set_virtual_machine(self, virtual_machine):
        self._virtual_machine = virtual_machine