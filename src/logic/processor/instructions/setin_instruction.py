from logic.processor.instructions.instruction_simple_arg import InstructionSimpleArg

class SetInInstruction(InstructionSimpleArg):

    def __init__(self, token, address, argument1=None):
        super().__init__(token.lexeme, token, address, argument1)

    
    def execute(self, processor):
        pass # TODO leer input del usuario y guardarlo en la 
    # memoria D, específicamente, en la direccion resultante
    # de evaluar la expresión destino