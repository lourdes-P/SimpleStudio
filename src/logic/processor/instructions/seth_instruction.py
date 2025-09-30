from logic.processor.instructions.instruction_double_arg import InstructionDoubleArg
from logic.expression_ast.exceptions.datacell_value_notset_exception import DatacellValueNotSetException
from logic.expression_ast.exceptions.heapcell_value_notset_exception import HeapcellValueNotSetException
from logic.processor.exceptions.instruction_amalgam_exception import InstructionAmalgamException

class SetHInstruction(InstructionDoubleArg):

    def __init__(self, token, address, argument1=None, argument2=None):
        super().__init__(token.lexeme, token, address, argument1, argument2)

    
    def execute(self, processor):
        try:
            target_address = self.argument1.evaluate(processor)
            data = self.argument2.evaluate(processor)
        except (HeapcellValueNotSetException, DatacellValueNotSetException) as error_message:
            raise InstructionAmalgamException(error_message, self.address, self.line)
        
        processor.set_in_heap_memory(target_address, data)
        
        return processor.SUCCESS
    