from logic.interpreter.syntacticanalyzer.syntacticexceptions.syntacticexception_simple import SimpleSyntacticException

class StringInvalidComparationSyntacticException(SimpleSyntacticException):
    DEBUG = False
    def __init__(self, current_token):
        error_message = f"Syntactic error in line {current_token.line_number}, column {current_token.first_char_index}. A string can only be compared with a string."
        if self.DEBUG:
            error_message+= f"\n\n[Error:{current_token.lexeme}|{current_token.line_number}]"
        super().__init__(error_message)