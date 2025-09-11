from logic.interpreter.syntacticanalyzer.syntacticexceptions.syntacticexception_simple import SimpleSyntacticException

class DuplicatedLabelSyntacticException(SimpleSyntacticException):
    
    def __init__(self, label_token):
        error_message = f"At line {label_token.line}: label with name {label_token.token_name} has already been declared."
        super().__init__(error_message)