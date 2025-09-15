

class Processor:
    SUCCESS = 0
    FAILURE_DISABLED = 1
    FAILURE = 2
    
    def __init__(self, virtual_machine = None):
        self._virtual_machine = virtual_machine
        self._pc = 0
        self._actual = 0
        self._libre = 0
        self._po = 0   
        self._enabled = True     
        self._next_instruction = None
    
    def reset(self):
        self._pc = 0
        self._actual = 0
        self._libre = 0
        self._po = 0   
        self._enabled = True 
        self._next_instruction = None
    
    def execute_next_instruction(self):
        self._next_instruction = self.get_next_instruction()
        if self._next_instruction and self._enabled:
            success = self._next_instruction.execute()
            return success
        elif not self._enabled:
            return self.FAILURE_DISABLED
        else:
            return self.FAILURE
        
    def get_next_instruction(self):
        return self._virtual_machine.get_instruction(self._pc)
    
    def access_data_memory(self, address):
        return self._virtual_machine.access_data_memory(address) #TODO review mechanic
    
    def access_heap_memory(self, address):
        return self._virtual_machine.access_heap_memory(address)
    
    def set_in_data_memory(self, address, data):
        self._virtual_machine.set_data_memory(address, data)
    
    def set_in_heap_memory(self, address, data):
        self._virtual_machine.set_heap_memory(address, data)
    
    def trigger_user_input(self):
        self._virtual_machine.trigger_user_input()
        self.disable()
    
    def deliver_user_input(self):
        self._next_instruction.on_user_input()
        self.enable()
        
    def get_user_input(self):
        self._virtual_machine.get_user_input()
    
    def define_label(self, label_token, address):
        return self._virtual_machine.define_label(label_token, address)
    
    def disable(self):
        self._enabled = False
        self._virtual_machine.disable_execution()
        
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
