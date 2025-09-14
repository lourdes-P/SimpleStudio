from logic.processor.instructions.instruction_double_arg import InstructionDoubleArg

class SetHInstruction(InstructionDoubleArg):

    def __init__(self, token, address, argument1=None, argument2=None):
        super().__init__(token.lexeme, token, address, argument1, argument2)

    
    def execute(self, processor):
        pass # TODO
    # seth destino, fuente
    