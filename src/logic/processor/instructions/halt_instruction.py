from logic.processor.instructions.instruction import Instruction

class HaltInstruction(Instruction):

    def __init__(self, signature_token, address):
        super().__init__(signature_token.lexeme, signature_token, address)

    
    def execute(self, processor):
        processor.disable()
        return processor.SUCCESS
    