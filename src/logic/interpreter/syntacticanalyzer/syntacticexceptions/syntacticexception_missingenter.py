from logic.interpreter.syntacticanalyzer.syntacticexceptions.syntacticexception_simple import SimpleSyntacticException

class SyntacticExceptionMissingEnter(SimpleSyntacticException):
    
    def __init__(self, current_token):
        error_message = f"At line {current_token.line}: missing enter after instruction."
        super().__init__(error_message)