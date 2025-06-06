
class SyntacticException(Exception):
    # throw con: raise SyntacticException( , )
    def __init__(self, current_token, expected_token_name_list):
        expected_token_name_list_tostring = ", ".join(expected_token_name_list)
        error_message = f"Syntactic error in line {current_token.line_number}, column {current_token.first_char_index}. Expected: {expected_token_name_list_tostring}. Encountered: {current_token.lexeme}." + f"\n[Error:{current_token.lexeme}|{current_token.line_number}]"
        super().__init__(error_message)
