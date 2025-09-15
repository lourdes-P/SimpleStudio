from logic.processor.instructions.instruction_double_arg import InstructionDoubleArg

class SetLabelInstruction(InstructionDoubleArg):

    def __init__(self, token, address, argument1=None, argument2=None):
        super().__init__(token.lexeme, token, address, argument1, argument2)

    
    def execute(self, processor):
        label_token = self.argument1.subexpression_node.token
        value = self.argument2.evaluate(processor)
        success = processor.define_label(label_token, value)
        
        return success
        
    # setlabel identificador, fuente
    # se necesita una funcion en procesador que le pregunte a la virtual machine
    
    def generate_string(self):
        return (f"{self.name} {self.argument1.lexeme}, {self.argument2.generate_string()}")  