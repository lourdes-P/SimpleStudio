
class EmptyCacheException(Exception):
    
    def __init__(self):
        error_message = f"Attempted to retrieve from empty cache."
        super().__init__(error_message)