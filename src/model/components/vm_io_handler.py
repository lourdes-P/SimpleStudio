
class VMIOHandler:
    
    def __init__(self):
        self._last_output_text = ''
        self._last_user_input = ''
        
    def reset(self):
        self._last_output_text = ''
        self._last_user_input = ''
    
    def set_last_output(self, text):
        self._last_output_text = text
        
    def get_last_output(self):
        return self._last_output_text
    
    def set_last_user_input(self, input):
        self._last_user_input = input
    
    def get_last_user_input(self):
        return self._last_user_input