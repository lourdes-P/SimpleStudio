import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog
from view.components.controlpanel import ControlPanel
from view.components.memorypanel import MemoryPanel

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
        
        self.control_panel = ControlPanel(self, change_appearance_mode= self.change_appearance_mode, browse_file= self.browse_file)
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

    def get_code_memory_view(self):
        return self.memory_panel.get_code_memory_view()
    
    def load_code_onto_c_memory(self, code_data):
        self.memory_panel.load_code_onto_c_memory(code_data)
        
    def on_breakpoint_change(self, line_num: int, is_set: bool):
            """Example breakpoint change handler"""
            status = "set" if is_set else "cleared"
            print(f"Breakpoint at line {line_num} {status}")
            
    def get_breakpoints(self):
        return self.code_memory_view.get_breakpoints()
    
    def browse_file(self):
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
        
    def run_code(self):
        # Placeholder for run functionality
        self.output_text.configure(state="normal")
        self.output_text.insert("end", "Running code...\n")
        self.output_text.configure(state="disabled")
        
    def step_code(self):
        # Placeholder for step functionality
        self.output_text.configure(state="normal")
        self.output_text.insert("end", "Stepping through code...\n")
        self.output_text.configure(state="disabled")
        
    def reset_vm(self):
        # Placeholder for reset functionality
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("end", "VM reset.\n")
        self.output_text.configure(state="disabled")  
        
    def display_error(self, message):
        # TODO implement an error dialog here
        print(f"Error: {message}")      

if __name__ == "__main__":
    app = SimpleStudioView()
    app.mainloop()