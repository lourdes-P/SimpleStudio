from logic.compiler.syntacticanalyzer.syntacticexceptions.syntacticexception import SyntacticException

class SyntacticExceptionNoMatch(SyntacticException):

    def __init__(self, current_token, expected_token_name):
        expected_token_name_list = [ expected_token_name ]
        super().__init__(current_token, expected_token_name_list)