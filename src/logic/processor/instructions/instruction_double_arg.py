from logic.processor.instructions.instruction_simple_arg import InstructionSimpleArg

class InstructionDoubleArg(InstructionSimpleArg):

    def __init__(self, name, signature_token, address, argument1=None, argument2=None):
        super().__init__(name, signature_token, address, argument1)
        self._argument2 = argument2

    def set_argument2(self, argument2):
        self._argument2 = argument2

    @property
    def argument2(self):
        return self._argument2

    