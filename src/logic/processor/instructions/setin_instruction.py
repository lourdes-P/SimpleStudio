from logic.processor.instructions.instruction_simple_arg import InstructionSimpleArg

class SetInInstruction(InstructionSimpleArg):

    def __init__(self, token, address, argument1=None):
        super().__init__(token.lexeme, token, address, argument1)

    
    def execute(self, processor):
        target_address = self.argument1.evaluate(processor)
        input = processor.get_user_input()
        processor.save_in_data_memory(target_address, input)
        return processor.SUCCESS
        # TODO leer input del usuario y guardarlo en la 
    # memoria D, específicamente, en la direccion resultante
    # de evaluar la expresión destino