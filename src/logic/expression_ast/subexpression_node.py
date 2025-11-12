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
    
    def _get_type(self, object_):
        """Gets type of object (evaluation of argument of a node), which can be (and should be) either string or int"""
        return 'string' if object_.__class__.__name__ == str.__name__ else 'int'