from logic.processor.instructions.instruction_double_arg import InstructionDoubleArg

class SetLabelInstruction(InstructionDoubleArg):

    def __init__(self, token, address, argument1=None, argument2=None):
        super().__init__(token.lexeme, token, address, argument1, argument2)

    
    def execute(self, processor):
        pass # TODO
    
    def generate_string(self):
        return (f"{self.name} {self.argument1.lexeme}, {self.argument2.generate_string()}")  