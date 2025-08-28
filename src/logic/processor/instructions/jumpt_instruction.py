from logic.processor.instructions.instruction_double_arg import InstructionDoubleArg

class JumpTInstruction(InstructionDoubleArg):

    def __init__(self, token, address, name, signature_token, argument1=None, argument2=None):
        super().__init__(name, signature_token, address, argument1, argument2)

    def execute(self, processor):
        pass # TODO