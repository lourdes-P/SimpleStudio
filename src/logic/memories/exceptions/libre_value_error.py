from logic.memories.exceptions.register_value_error import RegisterValueError

class LibreValueError(RegisterValueError):
    
    def __init__(self, libre_value):
        super().__init__(register_name='Libre', register_value=libre_value)