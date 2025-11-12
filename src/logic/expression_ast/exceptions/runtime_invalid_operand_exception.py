
class RuntimeInvalidOperandException(Exception):
    def __init__(self, operator_token, invalid_type_name, expression_evaluation):
        newline = '\n'
        error_message= f"Invalid '{invalid_type_name}' literal with operator '{operator_token.lexeme}': '{expression_evaluation}'."
        super().__init__(error_message)