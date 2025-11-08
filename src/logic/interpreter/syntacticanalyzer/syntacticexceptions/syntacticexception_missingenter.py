from logic.interpreter.syntacticanalyzer.syntacticexceptions.syntacticexception_simple import SimpleSyntacticException

class SyntacticExceptionMissingEnter(SimpleSyntacticException):
    DEBUG= False
    def __init__(self, current_token):
        error_message = f"At line {current_token.line_number}: missing enter after instruction."
        if self.DEBUG:
            error_message+= f"\n\n[Error:{current_token.lexeme}|{current_token.line_number}]"
        super().__init__(error_message)