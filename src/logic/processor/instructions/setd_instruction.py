from logic.processor.instructions.instruction_double_arg import InstructionDoubleArg

class SetDInstruction(InstructionDoubleArg):

    def __init__(self, token, address, argument1=None, argument2=None):
        super().__init__(token.lexeme, token, address, argument1, argument2)

    
    def execute(self, processor):
        target_address = self.argument1.evaluate(processor)
        data = self.argument2.evaluate(processor)
        processor.set_in_data_memory(target_address, data)
        
        return processor.SUCCESS
