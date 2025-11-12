from logic.interpreter.syntacticanalyzer.syntacticexceptions.syntacticexception_simple import SimpleSyntacticException

class StringInvalidOperatorSyntacticException(SimpleSyntacticException):
    DEBUG = False
    def __init__(self, current_token):
        error_message = f"Syntactic error in line {current_token.line_number}, column {current_token.first_char_index}. Invalid operator for string operand."
        if self.DEBUG:
            error_message+= f"\n\n[Error:{current_token.lexeme}|{current_token.line_number}]"
        super().__init__(error_message)