from abc import ABC, abstractmethod

class Instruction(ABC):

    def __init__(self, name, signature_token, address = None):
        self._name = name
        self._signature_token = signature_token
        self._line = signature_token.line_number
        self._address = address

    def set_address(self, address):
        self._address = address

    @property
    def name(self):
        return self._name
    
    @property
    def signature_token(self):
        return self._signature_token
    
    @property
    def line(self):
        return self._line
    
    @property
    def address(self):
        return self._address

    @abstractmethod
    def execute(self, processor):
        pass
    
    def generate_string(self):
        return self.name
