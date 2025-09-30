from logic.processor.instructions.instruction_double_arg import InstructionDoubleArg
from logic.expression_ast.exceptions.datacell_value_notset_exception import DatacellValueNotSetException
from logic.expression_ast.exceptions.heapcell_value_notset_exception import HeapcellValueNotSetException
from logic.processor.exceptions.instruction_amalgam_exception import InstructionAmalgamException

class SetLabelInstruction(InstructionDoubleArg):

    def __init__(self, token, address, argument1=None, argument2=None):
        super().__init__(token.lexeme, token, address, argument1, argument2)

    
    def execute(self, processor):
        label_token = self.argument1
        try:
            value = self.argument2.evaluate(processor)
        except (HeapcellValueNotSetException, DatacellValueNotSetException) as error_message:
            raise InstructionAmalgamException(error_message, self.address, self.line)
        
        success = processor.define_label(label_token, value)
        
        return success
    
    def generate_string(self):
        return (f"{self.name} {self.argument1.lexeme}, {self.argument2.generate_string()}")  