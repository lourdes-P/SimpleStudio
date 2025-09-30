from logic.processor.exceptions.instruction_amalgam_exception import InstructionAmalgamException

class Processor:
    COMPLETED = 0
    DISABLED = 1
    FAILURE = 2
    SUCCESS = 3
    
    def __init__(self, virtual_machine = None):
        self._virtual_machine = virtual_machine
        self._former_pc = 0
        self._pc = self._former_pc
        self._actual = 0
        self._libre = 0
        self._po = 0   
        self._enabled = False
        self.enable()    
        self._next_instruction = None
        self._error = None
    
    def reset(self):
        self._pc = 0
        self._actual = 0
        self._libre = 0
        self._po = 0   
        self.enable()
        self._next_instruction = None
        self._error = None
    
    def execute_next_instruction(self):
        self._next_instruction = self.get_next_instruction()
        if self._next_instruction and self._enabled:
            exception_caught = False
            try:
                success = self._next_instruction.execute(self)
            except InstructionAmalgamException as error:
                exception_caught = True
                self._error = error
            finally:
                if exception_caught:
                    self._enabled = False
                    return self.FAILURE
                
            if success == self.SUCCESS and self._former_pc == self._pc:
                self.increase_pc()
            elif success == self.SUCCESS:
                self._former_pc = self._pc

            return success
        elif not self._enabled:
            return self.DISABLED
        else:
            return self.FAILURE
        
    def get_next_instruction(self):
        return self._virtual_machine.get_instruction(self._pc)
    
    def get_label_address(self, label_name):
        return self._virtual_machine.get_label_address(label_name)
    
    def access_data_memory(self, address):
        return self._virtual_machine.access_data_memory(address) #TODO review mechanic
    
    def access_heap_memory(self, address):
        return self._virtual_machine.access_heap_memory(address)
    
    def set_in_data_memory(self, address, data):
        self._virtual_machine.set_data_memory(address, data, self._pc)
    
    def set_in_heap_memory(self, address, data):
        self._virtual_machine.set_heap_memory(address, data, self._pc)
    
    def trigger_user_input(self):
        self.disable()
        self._virtual_machine.trigger_user_input()
        
    def deliver_user_input(self):
        state = self._next_instruction.on_user_input(self)
        if state == self.SUCCESS:
            self.enable()
        
    def get_user_input(self):
        return self._virtual_machine.get_user_input()
    
    def define_label(self, label_token, address):
        return self._virtual_machine.define_label(label_token, address)
    
    def print_output(self, text):
        self._virtual_machine.print_output(text)
    
    def disable(self):
        self._enabled = False
        self._virtual_machine.disable_execution()
        
    def enable(self):
        self._enabled = True
        self._virtual_machine.enable_execution()
        
    def set_actual(self, address):
        former = self._actual
        self._actual = address
        self._virtual_machine.set_actual(former, self._actual)
        
    def set_libre(self, address):
        former = self._libre
        self._libre = address
        self._virtual_machine.set_libre(former, self._libre)
        
    def set_po(self, address):
        former = self._po
        self._po = address
        self._virtual_machine.set_po(former, self._po)
        
    def set_pc(self, address):
        self._pc = address
        
    def increase_pc(self):
        self._pc += 1
        self._former_pc = self._pc
        
    def get_error(self):
        return self._error
    
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
