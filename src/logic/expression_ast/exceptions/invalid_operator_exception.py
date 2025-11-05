
class InvalidOperatorException(Exception):
    def __init__(self, operator_token, left_side_class_name, right_side_class_name):
        newline = '\n'
        error_message= f"Operator '{operator_token.lexeme}' cannot be applied to '{left_side_class_name}', '{right_side_class_name}'.{newline}Error in line {operator_token.line_number}, column {operator_token.first_char_index}"
        super().__init__(error_message)