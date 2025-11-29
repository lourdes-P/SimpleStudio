

class BreakpointManager:
    
    def __init__(self):
        self._breakpoint_list = None
        
    def reset(self):
        self._breakpoint_list = None
        
    def update_breakpoint_list(self, breakpoint_list):
        self._breakpoint_list = breakpoint_list
        
    def address_in_breakpoint_list(self, address: int):
        return self._breakpoint_list != None and address in self._breakpoint_list
    