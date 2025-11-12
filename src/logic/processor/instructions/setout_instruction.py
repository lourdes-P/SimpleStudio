from logic.processor.instructions.instruction_simple_arg import InstructionSimpleArg

class SetOutInstruction(InstructionSimpleArg):

    def __init__(self, token, address, argument1=None):
        super().__init__(token.lexeme, token, address, argument1)

    
    def execute(self, processor):
        argument = self.argument1.evaluate(processor)
        
        processor.print_output(argument)
        return processor.SUCCESS
