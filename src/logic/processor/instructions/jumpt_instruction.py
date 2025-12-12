from logic.processor.exceptions.runtime_jump_address_invalid_exception import RuntimeJumpAddressInvalidException
from logic.processor.instructions.instruction_double_arg import InstructionDoubleArg

class JumpTInstruction(InstructionDoubleArg):

    def __init__(self, signature_token, address, argument1=None, argument2=None):
        super().__init__(signature_token.lexeme, signature_token, address, argument1, argument2)

    def execute(self, processor):
        address = self.argument1.evaluate(processor)
        conditional = self.argument2.evaluate(processor)
        
        if conditional:
            try:
                processor.set_pc(address)
            except ValueError:
                raise RuntimeJumpAddressInvalidException(address) 
        
        return processor.SUCCESS