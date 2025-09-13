from logic.interpreter.syntacticanalyzer.syntacticexceptions.syntacticexception_simple import SimpleSyntacticException

class DuplicatedLabelSyntacticException(SimpleSyntacticException):
    
    def __init__(self, label_token):
        error_message = f"At line {label_token.line_number}: label with name {label_token.lexeme} has already been declared."
        super().__init__(error_message)