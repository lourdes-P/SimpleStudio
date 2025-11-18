class InvalidMemoryAccessOperandException(Exception):
    def __init__(self, token, expression, invalid_type_name):
        newline = '\n'
        error_message= f"Invalid '{invalid_type_name}' literal within memory access expression: '{expression.generate_string()}'.{newline}Error in line {token.line_number}, column {token.first_char_index}."
        super().__init__(error_message)