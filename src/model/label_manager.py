
from logic.processor.processor import Processor

class LabelManager:
    def __init__(self):
        self._code_label_dictionary = None
        self._label_dictionary = None
        self._last_execution_added_labels = {}
        self._deleted_label_name = None
        
    def reset(self, on_load = True):
        self._deleted_label_name = None
        self._last_execution_added_labels.clear()
        if not on_load:
            if self._code_label_dictionary is not None:
                    self._label_dictionary = self._code_label_dictionary.copy()
        
    def define_label(self, label_token, address, cache):
        label_name = str.lower(label_token.lexeme)
        if self._code_label_dictionary.get(label_name) == None:  
            former_address = self._label_dictionary.get(label_name)
            cache.peek().set_label_added_entry({label_name : former_address})
            self._label_dictionary[label_name] = address
            self._last_execution_added_labels[label_name] = address
            return Processor.SUCCESS
        else:
            return f"Label with name {label_name} is already defined in the code memory."

    def undo_label_modification(self, label_entry : dict):
        if label_entry is not None:
            label_name_former_address_tuple = label_entry.popitem()
            label_name = label_name_former_address_tuple[0]
            former_address = label_name_former_address_tuple[1]
            if former_address is None:
                if self._label_dictionary.get(label_name) is not None: 
                    self._label_dictionary.pop(label_name)
                    self._deleted_label_name = label_name
            else:
                self._label_dictionary[label_name] = former_address
                self._last_execution_added_labels[label_name] = former_address
    
    def set_label_dictionary(self, label_dictionary : dict):
        self._code_label_dictionary = label_dictionary
        self._label_dictionary = self._code_label_dictionary.copy()
        
    def get_code_label_value(self, label_name):
        return self._code_label_dictionary.get(label_name)
    
    def clear_last_execution_added_labels(self):
        self._last_execution_added_labels.clear()
        
    def get_last_execution_added_labels(self):
        return self._last_execution_added_labels.copy()
    
    def get_label_address(self, label_name):
        address = self._label_dictionary.get(str.lower(label_name))
        return address
    
    def get_label_dictionary(self):
        return self._label_dictionary
    
    def get_deleted_label_name(self):
        return self._deleted_label_name
    