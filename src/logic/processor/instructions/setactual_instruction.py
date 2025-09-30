from logic.processor.instructions.instruction_simple_arg import InstructionSimpleArg
from logic.expression_ast.exceptions.datacell_value_notset_exception import DatacellValueNotSetException
from logic.expression_ast.exceptions.heapcell_value_notset_exception import HeapcellValueNotSetException
from logic.processor.exceptions.instruction_amalgam_exception import InstructionAmalgamException

class SetActualInstruction(InstructionSimpleArg):

    def __init__(self, token, address, argument1=None):
        super().__init__(token.lexeme, token, address, argument1)

    
    def execute(self, processor):
        try:
            address = self.argument1.evaluate(processor)
        except (HeapcellValueNotSetException, DatacellValueNotSetException) as error_message:
            raise InstructionAmalgamException(error_message, self.address, self.line)

        processor.set_actual(address)
        return processor.SUCCESS