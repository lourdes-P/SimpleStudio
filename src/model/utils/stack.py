from typing import List

class Stack(List):
    
    def push(self, entry):
        self.append(entry)
    
    def peek(self):
        if not self.is_empty():
            return self[-1]
        else:
            pass    # TODO exception?
        
    def pop(self):
        if not self.is_empty():
            return super().pop()
        else:
            pass
    
    def size(self):
        return len(self)
        
    def is_empty(self):
        return not bool(self)