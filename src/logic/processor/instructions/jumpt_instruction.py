from logic.processor.instructions.instruction_double_arg import InstructionDoubleArg
from logic.expression_ast.exceptions.datacell_value_notset_exception import DatacellValueNotSetException
from logic.expression_ast.exceptions.heapcell_value_notset_exception import HeapcellValueNotSetException
from logic.processor.exceptions.instruction_amalgam_exception import InstructionAmalgamException

class JumpTInstruction(InstructionDoubleArg):

    def __init__(self, signature_token, address, argument1=None, argument2=None):
        super().__init__(signature_token.lexeme, signature_token, address, argument1, argument2)

    def execute(self, processor):
        try:
            address = self.argument1.evaluate(processor)
            conditional = self.argument2.evaluate(processor)
        except (HeapcellValueNotSetException, DatacellValueNotSetException) as error_message:
            raise InstructionAmalgamException(error_message, self.address, self.line)
        
        if conditional:
            processor.set_pc(address)
        
        return processor.SUCCESS