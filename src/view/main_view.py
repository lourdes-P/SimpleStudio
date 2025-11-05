import customtkinter as ctk
from tkinter import filedialog
from view.components.controlpanel import ControlPanel
from view.components.input_dialog import InputDialog
from view.components.labelpanel import LabelPanel
from view.components.memorypanel import MemoryPanel
from CTkMessagebox import CTkMessagebox

from view.components.output_panel import OutputPanel
from view.utils.color_manager import ColorManager

# Set appearance mode and color theme
ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # "blue", "green", "dark-blue"

class SimpleStudioView(ctk.CTk):
        
    def __init__(self, presenter):
        super().__init__()
        
        self.title("SimpleStudio")
        self.geometry("1200x800")
        self.minsize(800,600)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        self.control_panel = None
        self.memory_panel = None
        self.label_panel = None    
        self._output_panel = None
        
        self.presenter = presenter
        
        self._create_widgets()
        self._setup_bindings()
        
    def _create_widgets(self):
        # Create main grid - now with a row for the top sidebar
        self.grid_columnconfigure((1,2), weight=1)  # Single column for main content
        self.grid_columnconfigure(0, weight=0)  # Single column for main content
        self.grid_rowconfigure(1, weight=1)     # Main content area gets the weight
        self.grid_rowconfigure(2, weight=0)
        
        self.control_panel = ControlPanel(self, step_callback= self.presenter.on_single_step_execution,
                                          run_callback= self.presenter.on_complete_execution,
                                          n_step_callback= self.presenter.on_n_step_execution,
                                          reset_callback=self.presenter.on_reset,
                                          undo_callback= self.presenter.on_undo,
                                          switch_code_editor_callback=self.presenter.on_switch_code_editor,
                                          change_appearance_mode= self.change_appearance_mode, 
                                          browse_file= self.on_browse_file,
                                          on_save_callback = self.on_save_file,
                                          on_save_as_callback = self.on_save_as_file)
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

    def _setup_bindings(self):
        self.bind_all("<Control-h>", lambda _: self.on_browse_file())
        self.bind_all("<Control-H>", lambda _: self.on_browse_file())
        self.bind_all("<Control-s>", lambda _: self.on_save_file())
        self.bind_all("<Control-S>", lambda _: self.on_save_file())
        self.bind_all("<Control-Shift-s>", lambda _: self.on_save_as_file())
        self.bind_all("<Control-Shift-S>", lambda _: self.on_save_as_file())
        self.bind_all("<Control-e>", lambda _: self.control_panel.switch_code_editor())
        self.bind_all("<Control-E>", lambda _: self.control_panel.switch_code_editor())
        self.bind_all("<F5>", lambda _: self.presenter.on_reset())
        self.bind_all("<F7>", lambda _: self.control_panel.on_undo())
        self.bind_all("<F8>", lambda _: self.control_panel.on_step())
        self.bind_all("<F9>", lambda _: self.control_panel.on_n_step())
        self.bind_all("<F10>", lambda _: self.control_panel.on_run())

    def set_pc(self, pc, last_executed_instruction_address):
        self.memory_panel.set_pc(pc, last_executed_instruction_address)

    def get_code_memory_view(self):
        return self.memory_panel.get_code_memory_view()
    
    def get_breakpoints(self):
        return self.memory_panel.get_breakpoints()
    
    def load_code_onto_c_memory(self, code_data, file_path, load_new_file, clear_breakpoints = True):
        self.memory_panel.load_code_onto_c_memory(code_data, file_path, load_new_file, clear_breakpoints)
        
    def load_code_editor(self, load_new_file):
        self.memory_panel.load_code_editor(self.get_selected_file_path(), load_new_file)
        
    def load_data_memory(self, data):
        self.memory_panel.load_data_memory(data)
        
    def load_heap_memory(self, data):
        self.memory_panel.load_heap_memory(data)
        
    def load_label_panel(self, label_list):
        self.label_panel.load_data(label_list)
        
    def add_labels(self, added_labels_list):
        self.label_panel.add_label_list(added_labels_list, ColorManager.SECONDARY_COLOR) 
      
    def delete_label(self, label_name) :
        self.label_panel.delete_label(label_name)
        
    def update_data_memory(self, modified_data_cells):
        self.memory_panel.update_data_memory(modified_data_cells)
        
    def update_heap_memory(self, modified_heap_cells):
        self.memory_panel.update_heap_memory(modified_heap_cells)
    
    def reset(self, parsed_data_memory, parsed_heap_memory, label_list, reset_code_memory = False):
        self.memory_panel.reset(parsed_data_memory, parsed_heap_memory, reset_code_memory)
        self.label_panel.reset(label_list)
        self._output_panel.reset()
        
    def switch_code_editor(self, line_number= None):
        self.memory_panel.switch_code_editor(line_number)
        
    def print_output(self, output_text):
        self._output_panel.append_text_ln(output_text)
    
    def on_browse_file(self):
        if self.memory_panel.code_editor_content_modified():
            if self.display_yes_no("Save file changes?", "Save?") == 'Yes':
                self.on_save_file()
        file_path = filedialog.askopenfilename(
            title="Select Source File",
            filetypes=[("All files", "*.*"),("Text files", "*.txt"),("SimpleSem files", "*.SimpleSem")]
        )
        
        if file_path:
            self.control_panel.set_file_path_label(file_path)            
            self.presenter.on_file_selected()
            
    def on_save_file(self):
        file_path = self.control_panel.get_file_path()
        if file_path is None or file_path == 'No file selected':
            self.on_save_as_file()
        else:
            content = self.memory_panel.get_code_editor_content()
            if not content:
                if self.display_yes_no("The content is empty. Do you want to save an empty file?") != 'Yes':
                    return
            self.presenter.on_save_file(content)
    
    def on_save_as_file(self):
        content = self.memory_panel.get_code_editor_content()
        if not content:
            if self.display_yes_no("The content is empty. Do you want to save an empty file?") != 'Yes':
                return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".SimpleStudio",
            filetypes=[("SimpleStudio files", "*.SimpleStudio"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        self.presenter.on_save_file(content, file_path=file_path)
        
    def on_save_code_editor(self):
        self.memory_panel.on_save_code_editor()
        
    def set_selected_file_path(self, file_path):
        self.control_panel.set_file_path_label(file_path)
    
    def get_selected_file_path(self):
        return self.control_panel.get_file_path()
        
    def get_selected_code_address(self):
        return self.memory_panel.get_selected_code_address()
        
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
    
    def display_yes_no(self, message, title = "Continue?"):
        yes_no_response = CTkMessagebox(
            title=title,
            message=message,
            icon="question",
            option_1="Yes",
            option_2="No",
            width= 300,
            height= 200,
            master=self
        )
        return yes_no_response.get()
        
    def display_user_input(self, on_user_input_callback):
        InputDialog.show_input_dialog(on_user_input_callback)
        
    def disable_execution(self):
        self.control_panel.set_buttons_state(False)
        
    def enable_execution(self):
        self.control_panel.set_buttons_state(True)
        
    def set_cache_entry_disponibility(self, number : int):
        if number >= 0:
            self.control_panel.set_cache_entry_disponibility(number)

    def _on_closing(self):
        if self.memory_panel.code_editor_content_modified():
            reply = self.display_yes_no("Save file changes?", "Save?")
            if reply == 'Yes':
                self.on_save_file()
            elif reply == 'No':
                pass
            else:
                return
        
        self.destroy()
        

if __name__ == "__main__":
    app = SimpleStudioView()
    app.mainloop()