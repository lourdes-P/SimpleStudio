
from model.exceptions.runtime_exception import RuntimeException

class DuplicatedLabelSyntacticException(RuntimeException):
    
    def __init__(self, label_token, address):
        error_message = f"At line {label_token.line_number}, address {address}: label with name {label_token.lexeme} has already been defined."
        super().__init__(error_message)