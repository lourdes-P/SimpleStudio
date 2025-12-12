from logic.processor.exceptions.runtime_jump_address_invalid_exception import RuntimeJumpAddressInvalidException
from logic.processor.instructions.instruction_simple_arg import InstructionSimpleArg

class JumpInstruction(InstructionSimpleArg):

    def __init__(self, token, address, argument1=None):
        super().__init__(token.lexeme, token, address, argument1)

    
    def execute(self, processor):
        address = self.argument1.evaluate(processor)
        
        try:
            processor.set_pc(address)
        except ValueError:
            raise RuntimeJumpAddressInvalidException(address)
        
        return processor.SUCCESS
    