from logic.interpreter.syntacticanalyzer.syntacticexceptions.syntacticexception_simple import SimpleSyntacticException

class InstructionInvalidStringArgumentSyntacticException(SimpleSyntacticException):
    DEBUG = False
    def __init__(self, current_token, argument_subexpression_string, instruction_type):
        error_message = f"Syntactic error in line {current_token.line_number}, column {current_token.first_char_index}. Invalid argument type for {instruction_type.upper()} instruction: string. Argument:" + f"\n{argument_subexpression_string}"
        if self.DEBUG:
            error_message+= f"\n\n[Error:{current_token.lexeme}|{current_token.line_number}]"
        super().__init__(error_message)