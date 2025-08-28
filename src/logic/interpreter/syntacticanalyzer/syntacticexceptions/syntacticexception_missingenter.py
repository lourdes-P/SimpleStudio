
class SyntacticExceptionMissingEnter(Exception):
    # throw con: raise SyntacticException( , )
    def __init__(self, current_token):
        error_message = f"At line {current_token.line}: missing enter after instruction."
        super().__init__(error_message)