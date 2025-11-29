
from abc import ABC, abstractmethod

class SimpleStudioViewInterface(ABC):
    
    @abstractmethod
    def start(self):
        """Start UI process."""
        pass
    
    @abstractmethod
    def set_pc(self, pc, last_executed_instruction_address):
        """Set PC on graphic code memory. Also sets last executed instruction address."""
        pass
    
    @abstractmethod
    def get_breakpoints(self):
        """Get breakpoint address list from graphic code memory."""
        pass
    
    @abstractmethod
    def load_code_onto_c_memory(self, code_data, file_path, load_new_file, clear_breakpoints = True):
        """
        Load code onto graphic C memory.
        Args: 
            code_data: parsed codecell list.
            file_path: file path corresponding to source code so that it can be shown on control panel and loaded onto code editor.
            load_new_file: True if a new file has been loaded.
            clear_breakpoints: True if file had to be reloaded due to modification or if a new file has been loaded.
        """
        pass
    
    @abstractmethod
    def load_code_editor(self, load_new_file):
        """
        Open code editor on selected file path. Purpose is to load the file onto the code editor after a parse error.
        Args:
            load_new_file: True if selected file has to be loaded.
        """
        pass
    
    @abstractmethod
    def load_data_memory(self, data):
        """
        Load parsed datacells onto graphic data memory.
        Args:
            data: list of dictionaries with keys (register, address, value, annotation, memory_modified).
        """
        pass
    
    @abstractmethod
    def load_heap_memory(self, data):
        """
        Load parsed heapcells onto graphic data memory.
        Args:
            data: list of dictionaries with keys (register, address, value, annotation, memory_modified).
        """
        pass
    
    @abstractmethod
    def load_label_panel(self, label_list):
        """
        Load parsed code label list onto graphic label panel.
        Args:
            label_list: list of dictionaries with keys (name, address).
        """
        pass
    
    @abstractmethod
    def add_labels(self, added_labels_list):
        """
        Load parsed dynamic label list of labels added/modified last execution onto graphic label panel.
        Args:
            added_labels_list: list of dictionaries with keys (name, address).
        """
        pass
    
    @abstractmethod
    def delete_label(self, label_name):
        """
        Delete from label panel the label whose name is label_name.
        Args:
            label_name: (string) name of label to delete.
        """
        pass
    
    @abstractmethod
    def update_data_memory(self, modified_data_cells):
        """
        Load parsed modified data cells onto graphic data memory.
        Args:
            modified_data_cells: list of dictionaries with keys (register, address, value, annotation, memory_modified).
        """
        pass
    
    @abstractmethod
    def update_heap_memory(self, modified_heap_cells):
        """
        Load parsed modified hrap cells onto graphic heap memory.
        Args:
            modified_heap_cells: list of dictionaries with keys (register, address, value, annotation, memory_modified).
        """
        pass
    
    @abstractmethod
    def reset(self, parsed_data_memory, parsed_heap_memory, label_list):
        """
        Reset graphic data memory, heap memory, label panel, and output panel.
        Args:
            parsed_data_memory: list of dictionaries with keys (register, address, value, annotation, memory_modified). Represents data memory. Only modified cells.
            parsed_heap_memory: list of dictionaries with keys (register, address, value, annotation, memory_modified). Represents heap memory. Only modified cells.
            label_list: list of dictionaries with keys (name, address).
        """
        pass
    
    @abstractmethod
    def switch_code_editor(self, line_number= None):
        """
        Switch from code editor to graphic code memory and viceversa.
        Args:
            line_number: line index to open code editor at the end of the line of index line_number.
        """
        pass
    
    @abstractmethod
    def print_output(self, output_text):
        """
        Print output in ouput panel.
        Args:
            output_text: (string) text to print.
        """
        pass
    
    @abstractmethod
    def on_save_code_editor(self):
        """
        Action triggered after saving code editor content. Initial content of code editor gets updated to current content.
        """
        pass
    
    @abstractmethod
    def set_selected_file_path(self, file_path):
        """
        Set selected file path on control panel to file_path.
        Args:
            file_path: file path to print in control panel.
        """
        pass
    
    @abstractmethod
    def get_selected_file_path(self):
        """
        Get selected file path by user.
        """
        pass
    
    @abstractmethod
    def get_selected_code_address(self):
        """
        Get index of selected row on graphic code memory. This index is then used to open code editor on corresponding line if user switches to code editor.
        """
        pass
    
    @abstractmethod
    def display_error(self, message):
        """
        Summon a Message box to show error on UI.
        Args:
            message: error message to show.
        """
        pass
    
    @abstractmethod
    def display_user_input(self, on_user_input_callback):
        """
        Display input dialog for user to write input. Once user enters input, function on_user_input_callback is called.
        Args:
            on_user_input_callback: callback funcion to call after user inputs value. Must have one argument to submit input to.
        """
        pass
    
    @abstractmethod
    def disable_execution(self):
        """
        Disables buttons linked to execution on control panel.
        """
        pass
    
    @abstractmethod
    def enable_execution(self):
        """
        Enables buttons linked to execution on control panel.
        """
        pass
    
    @abstractmethod
    def set_cache_entry_disponibility(self, number : int):
        """
        Set button Undo cache entry disponibility.
        Args:
            number: number of entries available in cache.
        """
        pass