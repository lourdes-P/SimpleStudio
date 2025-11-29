
from abc import ABC, abstractmethod

class SimpleStudioViewInterface(ABC):
    
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def set_pc(self):
        pass
    
    @abstractmethod
    def get_breakpoints(self):
        pass
    
    @abstractmethod
    def load_code_onto_c_memory(self, code_data, file_path, load_new_file, clear_breakpoints = True):
        pass
    
    @abstractmethod
    def load_code_editor(self, load_new_file):
        pass
    
    @abstractmethod
    def load_data_memory(self, data):
        pass
    
    @abstractmethod
    def load_heap_memory(self, data):
        pass
    
    @abstractmethod
    def load_label_panel(self, label_list):
        pass
    
    @abstractmethod
    def add_labels(self, added_labels_list):
        pass
    
    @abstractmethod
    def delete_label(self, label_name):
        pass
    
    @abstractmethod
    def update_data_memory(self, modified_data_cells):
        pass
    
    @abstractmethod
    def update_heap_memory(self, modified_heap_cells):
        pass
    
    @abstractmethod
    def reset(self, parsed_data_memory, parsed_heap_memory, label_list):
        pass
    
    @abstractmethod
    def switch_code_editor(self, line_number= None):
        pass
    
    @abstractmethod
    def print_output(self, output_text):
        pass
    
    @abstractmethod
    def on_save_code_editor(self):
        pass
    
    @abstractmethod
    def set_selected_file_path(self, file_path):
        pass
    
    @abstractmethod
    def get_selected_file_path(self):
        pass
    
    @abstractmethod
    def get_selected_code_address(self):
        pass
    
    @abstractmethod
    def display_error(self, message):
        pass
    
    @abstractmethod
    def display_user_input(self, on_user_input_callback):
        pass
    
    @abstractmethod
    def disable_execution(self):
        pass
    
    @abstractmethod
    def enable_execution(self):
        pass
    
    @abstractmethod
    def set_cache_entry_disponibility(self, number : int):
        pass