import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog
from view.components.codememory import CodeMemoryView

# Set appearance mode and color theme
ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # "blue", "green", "dark-blue"

class SimpleStudioView(ctk.CTk):
    def __init__(self, presenter):
        super().__init__()
        
        self.title("SimpleStudio")
        self.geometry("1200x800")
        
        # Initialize components
        self.code_memory_view = None
        self.presenter = presenter
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create main grid - now with a row for the top sidebar
        self.grid_columnconfigure(0, weight=1)  # Single column for main content
        self.grid_rowconfigure(1, weight=1)     # Main content area gets the weight
        
        # Create top sidebar frame (formerly sidebar)
        self.top_frame = ctk.CTkFrame(self, height=140, corner_radius=0)
        self.top_frame.grid(row=0, column=0, sticky="nsew")
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)  # Multiple columns for buttons
        
        # Top frame title
        self.logo_label = ctk.CTkLabel(
            self.top_frame, 
            text="",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), columnspan=2)
        
        # Control buttons - arranged horizontally
        self.run_button = ctk.CTkButton(
            self.top_frame, 
            text="Run",
            command=self.run_code
        )
        self.run_button.grid(row=0, column=2, padx=20, pady=10)
        
        self.step_button = ctk.CTkButton(
            self.top_frame, 
            text="Step",
            command=self.step_code
        )
        self.step_button.grid(row=0, column=3, padx=20, pady=10)
        
        self.reset_button = ctk.CTkButton(
            self.top_frame, 
            text="Reset",
            command=self.reset_vm
        )
        self.reset_button.grid(row=0, column=4, padx=20, pady=10)
        
        self.upload_button = ctk.CTkButton(
            self.top_frame,
            text="Upload Source",
            command=self.browse_file
        )
        self.upload_button.grid(row=0, column=5, padx=(20,0), pady=10)  
        
        self.file_path_label = ctk.CTkLabel(
            self.top_frame, 
            text="No file selected"
        )
        self.file_path_label.grid(row=0, column=6, padx=1, pady=10)    
        
        # Appearance mode option menu
        self.appearance_mode_label = ctk.CTkLabel(
            self.top_frame, 
            text="Appearance:",
            anchor="w"
        )
        self.appearance_mode_label.grid(row=0, column=7, padx=(20, 0), pady=10)
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.top_frame, 
            values=["System", "Dark", "Light"],
            command=self.change_appearance_mode,
            width=100
        )
        self.appearance_mode_optionemenu.grid(row=0, column=8, padx=(0, 20), pady=10)
        
        # Main content area - now below the top frame
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        # Add tabs
        self.tabview.add("Code")
        self.tabview.add("Memory")
        self.tabview.add("Output")
        
        # Configure tab weights to make them expand properly
        self.tabview.tab("Code").grid_rowconfigure(0, weight=1)
        self.tabview.tab("Code").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Memory").grid_rowconfigure(0, weight=1)
        self.tabview.tab("Memory").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Output").grid_rowconfigure(0, weight=1)
        self.tabview.tab("Output").grid_columnconfigure(0, weight=1)
        
        # Code tab
        self.code_text = ctk.CTkTextbox(self.tabview.tab("Code"), width=400)
        self.code_text.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.code_text.insert("0.0", "// Enter your intermediate code here\n")
        
        # Memory tab - using a frame with grid
        self.memory_frame = ctk.CTkFrame(self.tabview.tab("Memory"))
        self.memory_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.memory_frame.grid_rowconfigure(1, weight=1)  # Make the code memory expand
        self.memory_frame.grid_columnconfigure(0, weight=1)
                        
        self.create_c_memory()
        
        # Output tab
        self.output_text = ctk.CTkTextbox(self.tabview.tab("Output"), width=400)
        self.output_text.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.output_text.configure(state="disabled")  # Make it read-only
        
        
    def create_c_memory(self):        
        cmem_label = ctk.CTkLabel(self.memory_frame, text="C", font=ctk.CTkFont(weight="bold"))
        cmem_label.grid(row=0, column=0, padx=10, pady=1, sticky="w")
        # Create the code memory view and place it in the memory frame
        self.code_memory_view = CodeMemoryView(self.memory_frame)
        self.code_memory_view.grid(row=1, column=0, columnspan=2, padx=10, pady=1, sticky="nsew")
        
        self.code_memory_view.set_breakpoint_change_callback(self.on_breakpoint_change)
        self.code_memory_view.change_appearance_mode("System")
        #self.load_sample_code()
                
        
    def load_parsed_code(self):
        self._presenter.update_code_memory_view()
        
        # Update output to show success
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("end", "Code parsed successfully!\n")
        self.output_text.configure(state="disabled")

    def get_code_memory_view(self):
        return self.code_memory_view
        
    def load_sample_code(self):
            """Load sample intermediate code"""
            sample_code = [
                {'pc': 0, 'label': 'START', 'line': 1, 'instruction': 'LOAD R1, 10'},
                {'pc': 1, 'label': '', 'line': 2, 'instruction': 'ADD R1, R2'},
                {'pc': 2, 'label': 'LOOP', 'line': 3, 'instruction': 'SUB R1, 1'},
                {'pc': 3, 'label': '', 'line': 4, 'instruction': 'JNZ LOOP'},
                {'pc': 4, 'label': 'END', 'line': 5, 'instruction': 'HALT'},
                {'pc': 5, 'label': '', 'line': 6, 'instruction': 'DATA 0'},
                {'pc': 6, 'label': '', 'line': 7, 'instruction': 'DATA 0'},
            ]
            self.code_memory.load_code(sample_code)
        
    def on_breakpoint_change(self, line_num: int, is_set: bool):
            """Example breakpoint change handler"""
            status = "set" if is_set else "cleared"
            print(f"Breakpoint at line {line_num} {status}")
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Source File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            self.file_path_label.configure(text=file_path)            
            self.presenter.on_file_selected()
            
    def get_selected_file_path(self):
        return self.file_path_label.cget("text") if self.file_path_label else None
    
    def create_memory_table(self, parent, title, row):
        # Title
        label = ctk.CTkLabel(parent, text=title, font=ctk.CTkFont(weight="bold"))
        label.grid(row=row, column=0, columnspan=2, padx=10, pady=(20, 5), sticky="w")
        
        # Treeview for memory display
        columns = ("Address", "Value")
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=6)
        
        # Define headings
        tree.heading("Address", text="Address")
        tree.heading("Value", text="Value")
        
        # Define columns
        tree.column("Address", width=80, anchor="w")
        tree.column("Value", width=80, anchor="w")
        
        # Add some sample data
        for i in range(10):
            tree.insert("", "end", values=(f"0x{i:04X}", "0x00"))
        
        tree.grid(row=row+1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        
        return tree
        
    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
        self.code_memory_view.change_appearance_mode(new_appearance_mode)
        
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