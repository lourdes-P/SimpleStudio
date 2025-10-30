from typing import List

class Stack(List):
    
    def push(self, entry):
        self.append(entry)
    
    def peek(self):
        if not self.is_empty():
            return self[-1]
        else:
            return
        
    def pop(self):
        if not self.is_empty():
            return super().pop()
        else:
            return
    
    def size(self):
        return len(self)
        
    def is_empty(self):
        return len(self) == 0