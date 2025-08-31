from logic.processor.instructions.instruction_double_arg import InstructionDoubleArg

class JumpTInstruction(InstructionDoubleArg):

    def __init__(self, signature_token, address, argument1=None, argument2=None):
        super().__init__(signature_token.lexeme, signature_token, address, argument1, argument2)

    def execute(self, processor):
        pass # TODO