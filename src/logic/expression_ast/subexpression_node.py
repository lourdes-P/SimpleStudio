from abc import ABC, abstractmethod

class SubexpressionNode(ABC):

    @property
    @abstractmethod
    def token(self):
        pass

    def is_string(self):
        return False
    
    @abstractmethod
    def evaluate(self, processor=None):
        pass

    @abstractmethod
    def generate_string(self):
        pass