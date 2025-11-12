
class AddressValueInvalidException(Exception):
    
    def __init__(self, memory_name, address_value):
        error_message = f'Cannot work with {memory_name} memory address value with a value other than an integer. Input value: {address_value}.'
        super().__init__(error_message)