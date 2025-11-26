from logic.compiler.syntacticanalyzer.syntacticexceptions.syntacticexception_simple import SimpleSyntacticException

class DuplicatedLabelSyntacticException(SimpleSyntacticException):
    DEBUG= False
    def __init__(self, label_token):
        error_message = f"At line {label_token.line_number}: label with name {label_token.lexeme} has already been declared."
        if self.DEBUG:
            error_message+= f"\n\n[Error:{label_token.lexeme}|{label_token.line_number}]"
        super().__init__(error_message)