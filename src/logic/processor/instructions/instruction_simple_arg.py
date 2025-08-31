from logic.processor.instructions.instruction import Instruction

class InstructionSimpleArg(Instruction):

    def __init__(self, name, signature_token, address, argument1=None):
        super().__init__(name, signature_token, address)
        self._argument1 = argument1

    def set_argument1(self, argument1):
        self._argument1 = argument1

    @property
    def argument1(self):
        return self._argument1
    
    def generate_string(self):
        return f"{self.name} {self.argument1.generate_string()}"