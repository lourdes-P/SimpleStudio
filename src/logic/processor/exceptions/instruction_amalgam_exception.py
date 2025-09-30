
class InstructionAmalgamException(Exception):
    def __init__(self, former_error_message, address, line):
        newline= '\n'
        error_message= f"{former_error_message}{newline}Triggering instruction at address {address} in code memory, line {line} at source."
        super().__init__(error_message)