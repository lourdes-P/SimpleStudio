from logic.processor.instructions.instruction_simple_arg import InstructionSimpleArg


class SetInInstruction(InstructionSimpleArg):

    def __init__(self, token, address, argument1=None):
        super().__init__(token.lexeme, token, address, argument1)

    
    def execute(self, processor):
        processor.trigger_user_input()

        return processor.SUCCESS
    
    def on_user_input(self, processor):
        target_address = self.argument1.evaluate(processor)
            
        processor.set_in_data_memory(target_address, processor.get_user_input())
        return processor.SUCCESS