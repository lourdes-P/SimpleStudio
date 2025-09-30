import customtkinter as ctk
from tkinter import filedialog
from view.components.controlpanel import ControlPanel
from view.components.input_dialog import InputDialog
from view.components.labelpanel import LabelPanel
from view.components.memorypanel import MemoryPanel
from CTkMessagebox import CTkMessagebox

from view.components.output_panel import OutputPanel

# Set appearance mode and color theme
ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # "blue", "green", "dark-blue"

class SimpleStudioView(ctk.CTk):
    SECONDARY_COLOR = '#2c3e50'
    TERTIARY_COLOR = '#4b8bab'
        
    def __init__(self, presenter):
        super().__init__()
        
        self.title("SimpleStudio")
        self.geometry("1200x800")
        self.minsize(800,600)
        
        self.control_panel = None   # has top sidebar buttons (execution, upload code)
        self.memory_panel = None    # has the 3 memory frames (c, d, h)
        self.bottom_panel = None    # has label map (name, address) frame, output frame, test battery output frame
        self.presenter = presenter
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create main grid - now with a row for the top sidebar
        self.grid_columnconfigure((1,2), weight=1)  # Single column for main content
        self.grid_columnconfigure(0, weight=0)  # Single column for main content
        self.grid_rowconfigure(1, weight=1)     # Main content area gets the weight
        self.grid_rowconfigure(2, weight=0)
        
        self.control_panel = ControlPanel(self, step_callback= self.presenter.on_single_step_execution,
                                          run_callback= self.presenter.on_complete_execution,
                                          n_step_callback= self.presenter.on_n_step_execution,
                                          reset_callback=self.presenter.on_reset,
                                          change_appearance_mode= self.change_appearance_mode, 
                                          browse_file= self.on_browse_file)
        self.control_panel.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.control_panel.grid_rowconfigure(0, weight=1)
        self.control_panel.initialize()

        self.memory_panel = MemoryPanel(self)
        self.memory_panel.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")
        self.memory_panel.initialize(self.presenter.on_breakpoint_change)
        
        self.label_panel = LabelPanel(self)
        self.label_panel.grid(row=2, column=0, padx=5, pady=(0,10), sticky="sw")
        
        self._output_panel = OutputPanel(self)
        self._output_panel.grid(row=2, column=1, columnspan=2, padx=(0,5), pady=(0,10), sticky="nsew")

    def set_pc(self, pc, last_executed_instruction_address):
        self.memory_panel.set_pc(pc, last_executed_instruction_address)

    def get_code_memory_view(self):
        return self.memory_panel.get_code_memory_view()
    
    def get_breakpoints(self):
        return self.memory_panel.get_breakpoints()
    
    def load_code_onto_c_memory(self, code_data):
        self.memory_panel.load_code_onto_c_memory(code_data)
        
    def load_data_memory(self, data):
        self.memory_panel.load_data_memory(data)
        
    def load_heap_memory(self, data):
        self.memory_panel.load_heap_memory(data)
        
    def load_label_panel(self, label_list):
        self.label_panel.load_data(label_list)
        
    def add_labels(self, added_labels_list):
      self.label_panel.add_label_list(added_labels_list, self.SECONDARY_COLOR)  
        
    def update_data_memory(self, modified_data_cells):
        self.memory_panel.update_data_memory(modified_data_cells)
        
    def update_heap_memory(self, modified_heap_cells):
        self.memory_panel.update_heap_memory(modified_heap_cells)
    
    def reset(self, parsed_data_memory, parsed_heap_memory, label_list):
        self.memory_panel.reset(parsed_data_memory, parsed_heap_memory)
        self.label_panel.reset(label_list)
        self._output_panel.reset()
        
    def print_output(self, output_text):
        self._output_panel.append_text_ln(output_text)
    
    def on_browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Source File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            self.control_panel.set_file_path_label(file_path)            
            self.presenter.on_file_selected()
            
    def get_selected_file_path(self):
        return self.control_panel.get_file_path()
        
    def change_appearance_mode(self, new_appearance_mode):
        if new_appearance_mode != ctk.get_appearance_mode():
            ctk.set_appearance_mode(new_appearance_mode)
            self.memory_panel.change_appearance_mode(new_appearance_mode) 
        
    def display_error(self, message):
        error_box = CTkMessagebox(
            title="ERROR",
            message=message,
            icon="cancel",
            option_1="OK",
            width= 300,
            height= 200,
            master=self
        )    
        
    def display_user_input(self, on_user_input_callback):
        InputDialog.show_input_dialog(on_user_input_callback)
        
    def disable_execution(self):
        self.control_panel.set_buttons_state(False)
        
    def enable_execution(self):
        self.control_panel.set_buttons_state(True)

if __name__ == "__main__":
    app = SimpleStudioView()
    app.mainloop()