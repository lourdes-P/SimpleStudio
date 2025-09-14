from logic.processor.instructions.instruction_simple_arg import InstructionSimpleArg

class SetLibreInstruction(InstructionSimpleArg):

    def __init__(self, token, address, argument1=None):
        super().__init__(token.lexeme, token, address, argument1)

    
    def execute(self, processor):
        address = self.argument1.evaluate(processor)
        processor.set_libre(address)
        processor.increase_pc()
        return processor.SUCCESS