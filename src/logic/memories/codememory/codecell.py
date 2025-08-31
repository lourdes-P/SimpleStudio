from logic.interpreter.lexicalanalyzer.token_ import Token
class CodeCell:

    def __init__(self, label_token=None, address=None, instruction=None, annotation=None):
        self._label_token = label_token
        self._address = address
        self._instruction = instruction        
        self._annotation = annotation
    
    def set_label_token(self,label_token):
        self._label_token = label_token

    def set_address(self, address):
        self._address = address
        self._instruction.set_address(address)

    def set_instruction(self, instruction):
        self._instruction = instruction

    def set_annotation(self, annotation):
        self._annotation = annotation

    def print_codecell(self):
        print(f"label: {self.label_string()}, address: {self.address}, instruction: {self.instruction.generate_string()}, annotation: {self.annotation_string()}.")

    def label_string(self):
        return self._label_token.lexeme if self._label_token else ""
    
    def annotation_string(self):
        return self._annotation.lexeme if self._annotation else ""
    
    def str_instruction(self):
        instruction = ""
        for token in self._instruction:
            instruction += token.lexeme
        return instruction
    
    @property
    def label_token(self):
        return self._label_token
    
    @property
    def address(self):
        return self._address
    
    @property
    def instruction(self):
        return self._instruction
    
    @property
    def annotation(self):
        return self._annotation