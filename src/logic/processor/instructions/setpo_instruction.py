from logic.processor.instructions.instruction_simple_arg import InstructionSimpleArg

class SetPOInstruction(InstructionSimpleArg):

    def __init__(self, token, address, argument1=None):
        super().__init__(token.lexeme, token, address, argument1)

    
    def execute(self, processor): 
        address = self.argument1.evaluate(processor)
   
        processor.set_po(address)
        return processor.SUCCESS