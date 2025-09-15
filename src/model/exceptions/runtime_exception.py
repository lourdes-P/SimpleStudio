
class RuntimeException(Exception):
    
    def __init__(self, error):
        error_message = f"RUNTIME ERROR:\n {error}"
        super().__init__(error_message)