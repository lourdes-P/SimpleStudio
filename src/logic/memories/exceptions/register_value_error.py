
class RegisterValueError(Exception):
    
    def __init__(self, register_name, register_value):
        error_message = f'Cannot change {register_name} register with a value other than an integer. Input value: {register_value}'
        super().__init__(error_message)