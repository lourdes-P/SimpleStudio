from abc import ABC, abstractmethod

class SubexpressionNode(ABC):

    @property
    @abstractmethod
    def token(self):
        pass

    @abstractmethod
    def evaluate(self, processor=None):
        pass # TODO ver cómo evaluar los nodos de AST

    @abstractmethod
    def generate_string(self):
        pass