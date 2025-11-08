from logic.memories.exceptions.address_out_of_range import MemoryAddressOutOfRangeException
from logic.memories.exceptions.address_value_invalid_exception import AddressValueInvalidException
from logic.memories.exceptions.register_value_error import RegisterValueError
from logic.processor.exceptions.instruction_amalgam_exception import InstructionAmalgamException

class Processor:
    COMPLETED = 0
    DISABLED = 1
    FAILURE = 2
    SUCCESS = 3
    
    def __init__(self, virtual_machine = None):
        self._virtual_machine = virtual_machine
        self._enabled = False
        self._former_pc = 0
        self._pc = self._former_pc
        self._actual = 0
        self._libre = 0
        self._po = 0   
        self._next_instruction = None
        self._error = None
        self._after_execution_state = self.FAILURE
        self.enable()
    
    def reset(self):
        self._pc = 0
        self._former_pc = self._pc
        self._actual = 0
        self._libre = 0
        self._po = 0   
        self._next_instruction = None
        self._error = None
        self._after_execution_state = self.FAILURE
        self.enable()
    
    def execute_next_instruction(self):
        self._next_instruction = self._get_next_instruction()
        if self._next_instruction and self._enabled:
            try:
                self._after_execution_state = self._next_instruction.execute(self)
            except (InstructionAmalgamException, MemoryAddressOutOfRangeException, 
                    RegisterValueError, AddressValueInvalidException) as error:
                self._after_execution_state = self.FAILURE
                self._error = error
                self._enabled = False
                
            if self._after_execution_state == self.SUCCESS and self._former_pc == self._pc:
                self.increase_pc()
            elif self._after_execution_state == self.SUCCESS:
                self._former_pc = self._pc

            return self._after_execution_state
        elif not self._enabled:
            self._error = "Processor not enabled."
            return self.DISABLED
        elif self._next_instruction is None:
            self._error = "No instruction under current PC. Make sure to not try accessing an address out of code memory's range, and to halt execution properly with the HALT instruction."
            self._enabled = False
            return self.FAILURE
        else:
            self._enabled = False
            self._error = "ERROR in processor instruction execution."
            return self.FAILURE
        
    def _get_next_instruction(self):
        return self._virtual_machine.get_instruction(self._pc)
    
    def get_label_address(self, label_name):
        return self._virtual_machine.get_label_address(label_name)
    
    def access_data_memory(self, address):
        return self._virtual_machine.access_data_memory(address)
    
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
    
    def reinstate_pc(self, pc):
        self._former_pc = pc
        self._pc = pc
    
    def reinstate_actual(self, address):
        self._actual = address
        
    def reinstate_libre(self, address):
        self._libre = address
        
    def reinstate_po(self, address):
        self._po = address
    
    def disable(self):
        self._enabled = False
        self._virtual_machine.disable_execution()
        
    def enable(self):
        self._enabled = True
        self._error = None
        self._virtual_machine.enable_execution()
    
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
