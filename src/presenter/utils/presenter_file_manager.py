import os

class PresenterFileManager:
    
    def __init__(self):
        self._last_file_path = None
        self._file_last_modification_time = None
        self._loading_file = False
    
    def load_file(self, file_path):
        try:
            reset= False        
            self._loading_file = True
            if self._last_file_path is not None:
                reset = True
            self._last_file_path = file_path
            self._file_last_modification_time = os.path.getmtime(file_path)
            
            return reset
        except Exception as e:
            self._loading_file = False
            raise e
            
    def reload_file(self): 
        if self._last_file_path != None:
            file_modification_time = os.path.getmtime(self._last_file_path)
            if self._file_last_modification_time == file_modification_time:
                on_load = False
            else:
                self._loading_file = True
                self._file_last_modification_time = file_modification_time
                on_load = True
                
            return on_load
        else:
            return None
        
    def save(self, content):
        """Save the current content to the last used file path, if it is not None"""
        if self._last_file_path:
            self._write_to_file(self._last_file_path, content)
                
    def save_as(self, content, file_path):
        if file_path:
            self._write_to_file(file_path, content)
            self._last_file_path = file_path
                
    def _write_to_file(self, file_path, content):
        """Write content to the specified file path."""
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
       
    def set_loading_file(self, loading_file : bool):
        self._loading_file = loading_file
     
    @property    
    def loading_file(self):
        return self._loading_file
    
    @property
    def file_last_modification_time(self):
        return self._file_last_modification_time
    
    @property
    def last_file_path(self):
        return self._last_file_path