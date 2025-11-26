from logic.compiler.syntacticanalyzer.syntacticexceptions.syntacticexception_simple import SimpleSyntacticException

class StringInvalidUnaryOperationSyntacticException(SimpleSyntacticException):
    DEBUG = False
    def __init__(self, current_token, operand):
        error_message = f"Syntactic error in line {current_token.line_number}, column {current_token.first_char_index}. A string cannot be part of a unary operation. Expression:" + f"\n{current_token.lexeme}{operand.generate_string()}"
        if self.DEBUG:
            error_message+= f"\n\n[Error:{current_token.lexeme}|{current_token.line_number}]"
        super().__init__(error_message)