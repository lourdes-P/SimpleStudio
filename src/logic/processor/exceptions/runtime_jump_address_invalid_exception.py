
class RuntimeJumpAddressInvalidException(Exception):

    def __init__(self, invalid_address):
        error_message = f"Address '{invalid_address}' is invalid for jump instruction."
        super().__init__(error_message)