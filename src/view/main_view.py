import customtkinter as ctk
from tkinter import filedialog
from view.components.controlpanel import ControlPanel
from view.components.input_dialog import InputDialog
from view.components.memorypanel import MemoryPanel
from CTkMessagebox import CTkMessagebox

# Set appearance mode and color theme
ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # "blue", "green", "dark-blue"

class SimpleStudioView(ctk.CTk):
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
        # TODO execution buttons unabled before source load
        
    def create_widgets(self):
        # Create main grid - now with a row for the top sidebar
        self.grid_columnconfigure(0, weight=1)  # Single column for main content
        self.grid_rowconfigure(1, weight=1)     # Main content area gets the weight
        
        self.control_panel = ControlPanel(self, step_callback= self.presenter.on_single_step_execution,
                                          run_callback= self.presenter.on_complete_execution,
                                          n_step_callback= self.presenter.on_n_step_execution,
                                          change_appearance_mode= self.change_appearance_mode, browse_file= self.on_browse_file)
        self.control_panel.grid(row=0, column=0, sticky="nsew")
        self.control_panel.grid_rowconfigure(0, weight=1)
        self.control_panel.initialize()
        
        # Memory frame 
        # TODO clase de frame de memorias (extiende a customtkinter.CTkFrame)
        self.memory_panel = MemoryPanel(self)
        self.memory_panel.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.memory_panel.initialize()
        
    def load_parsed_code(self):
        self._presenter.update_code_memory_view()
        
        # Update output to show success
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("end", "Code parsed successfully!\n")
        self.output_text.configure(state="disabled")

    def set_pc(self, pc):
        self.memory_panel.set_pc(pc)

    def get_code_memory_view(self):
        return self.memory_panel.get_code_memory_view()
    
    def get_breakpoints(self):
        return self.code_memory_view.get_breakpoints()
    
    def get_user_input(self):
        return None # TODO get user input
    
    def load_code_onto_c_memory(self, code_data):
        self.memory_panel.load_code_onto_c_memory(code_data)
        
    def load_data_memory(self, data):
        self.memory_panel.load_data_memory(data)
        
    def load_heap_memory(self, data):
        self.memory_panel.load_heap_memory(data)
        
    def update_data_memory(self, modified_data_cells):
        self.memory_panel.update_data_memory(modified_data_cells)
        
    def update_heap_memory(self, modified_heap_cells):
        self.memory_panel.update_heap_memory(modified_heap_cells)
        
    def on_breakpoint_change(self, line_num: int, is_set: bool):
        """Example breakpoint change handler"""
        status = "set" if is_set else "cleared"
        print(f"Breakpoint at line {line_num} {status}")
            
    def on_run(self):
        pass
    
    def on_single_step(self):
        pass
    
    def on_n_step(self, n):
        pass
    
    def on_reset(self):
        pass
    
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
         
    def reset_vm(self):
        # Placeholder for reset functionality
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("end", "VM reset.\n")
        self.output_text.configure(state="disabled")  
        
    def display_error(self, message):
        # TODO implement an error dialog here
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
        InputDialog.show_input_dialog(self, on_user_input_callback) # TODO checkear si anda bien (se testeo sin callback)
        
    def disable_execution(self):
        self.control_panel.set_buttons_state(False)
        
    def enable_execution(self):
        self.control_panel.set_buttons_state(True)

if __name__ == "__main__":
    app = SimpleStudioView()
    app.mainloop()