


class Processor:
    SUCCESS = 0
    FAILURE = 1
    
    def __init__(self, virtual_machine = None):
        self._virtual_machine = virtual_machine
        self._pc = 0
        self._actual = 0
        self._libre = 0
        self._po = 0   
        self._enabled = True     
    
    def reset(self):
        self._pc = 0
        self._actual = 0
        self._libre = 0
        self._po = 0   
        self._enabled = True 
    
    def execute_next_instruction(self):
        next_instruction = self.get_next_instruction()
        if next_instruction:
            success = next_instruction.execute()
            return success
        else:
            return self.FAILURE
        
    def get_next_instruction(self):
        return self._virtual_machine.get_instruction(self._pc)
    
    def access_data_memory(self, address):
        return self._virtual_machine.access_data_memory(address) #TODO review mechanic
    
    def access_heap_memory(self, address):
        return self._virtual_machine.access_heap_memory(address)
    
    def disable(self):
        self._enabled = False
        
    def enable(self):
        self._enabled = True
        
    def set_actual(self, address):
        self._actual = address
        
    def set_libre(self, address):
        self._libre = address
        
    def set_po(self, address):
        self._po = address
        
    def set_pc(self, address):
        self._pc = address
        
    def increase_pc(self):
        self._pc += 1
    
    @property
    def pc(self):
        return self._pc
    
    @property
    def actual(self):
        return self._actual
    
    @property
    def libre(self):
        return self._libre
    
    @property
    def po(self):
        return self._po
