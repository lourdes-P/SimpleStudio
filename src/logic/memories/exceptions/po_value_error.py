from logic.memories.exceptions.register_value_error import RegisterValueError

class PoValueError(RegisterValueError):
    
    def __init__(self, po_value):
        super().__init__(register_name='PO', register_value=po_value)