
class DatacellValueNotSetException(Exception):
    def __init__(self, address):
        error_message= f"Accessed data cell value at address {address} has not been set."
        super().__init__(error_message)
        