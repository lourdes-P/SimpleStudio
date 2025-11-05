from logic.memories.exceptions.register_value_error import RegisterValueError

class ActualValueError(RegisterValueError):
    
    def __init__(self, actual_value):
        super().__init__(register_name= 'Actual', register_value=actual_value)