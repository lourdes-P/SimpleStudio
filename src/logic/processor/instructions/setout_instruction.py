from logic.processor.instructions.instruction_simple_arg import InstructionSimpleArg

class SetOutInstruction(InstructionSimpleArg):

    def __init__(self, token, address, argument1=None):
        super().__init__(token.lexeme, token, address, argument1)

    
    def execute(self, processor):
        argument = self.argument1.evaluate(processor)
        print(argument)     # TODO hacer un print en el output de la view
        processor.increase_pc()
        return processor.SUCCESS
        # TODO un print de un entero. muestra por pantalla 
    #el resultado de evaluar la expresión Fuente