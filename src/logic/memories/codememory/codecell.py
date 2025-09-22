from logic.memories.memorycell import MemoryCell

class CodeCell(MemoryCell):

    def __init__(self, label_token=None, address=None, instruction=None, annotation=None):
        super().__init__(address, annotation)
        self._label_token = label_token
        self._instruction = instruction        
    
    def set_label_token(self,label_token):
        self._label_token = label_token

    def set_instruction(self, instruction):
        self._instruction = instruction

    def print_codecell(self):
        print(f"label: {self.label_string()}, address: {self.address}, instruction: {self.instruction.generate_string()}, annotation: {self.annotation_string()}.")

    def label_string(self):
        return self._label_token.lexeme if self._label_token else ""
    
    def str_instruction(self):
        instruction = ""
        for token in self._instruction:
            instruction += token.lexeme
        return instruction
    
    @property
    def label_token(self):
        return self._label_token
    
    @property
    def instruction(self):
        return self._instruction