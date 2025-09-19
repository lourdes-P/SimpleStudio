import customtkinter as ctk
from tkinter import ttk

class MemoryPanel(ctk.CTkFrame):
    """Component for displaying memory tables (C, D, or H)"""
    def __init__(self, master, title, columns, data, **kwargs):
        super().__init__(master, **kwargs)
        
        self.title = title
        self.columns = columns
        self.data = data
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_label = ctk.CTkLabel(self, text=self.title, font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(10, 15))
        
        # Create treeview (table)
        self.tree = ttk.Treeview(self, columns=self.columns, show='headings', height=10)
        
        # Define columns
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=(0, 10))
        scrollbar.pack(side='right', fill='y', padx=(0, 10), pady=(0, 10))
        
        # Insert data
        self.update_data(self.data)
    
    def update_data(self, new_data):
        """Update the table with new data"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        hmem_label = ctk.CTkLabel(self.hmem_container, text="H", font=ctk.CTkFont(weight="bold"))
        hmem_label.grid(row=0, column=0, padx=2, pady=(1,0), sticky="sw")
        self.heap_memory_view = DataHeapMemoryView(self.hmem_container)
        self.heap_memory_view.grid(row=1, column=0, padx=0, pady=1, sticky="nsew")
        
        self.paned_memory.add(self.hmem_container)
        
    def load_code_onto_c_memory(self, code_data):
        self.code_memory_view.load_code(code_data)
        
    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
        self.after(20, lambda: 
            self.paned_memory.configure(bg=self.get_single_color(self.cget("fg_color")))
        )
        self.code_memory_view.change_appearance_mode(new_appearance_mode)
        self.data_memory_view.change_appearance_mode(new_appearance_mode)
        self.heap_memory_view.change_appearance_mode(new_appearance_mode)  
      
    def get_code_memory_view(self):
        return self.code_memory_view        
        
    def on_breakpoint_change(self, line_num: int, is_set: bool):
            """Example breakpoint change handler"""
            status = "set" if is_set else "cleared"
            print(f"Breakpoint at line {line_num} {status}")
            
    def get_breakpoints(self):
        return self.code_memory_view.get_breakpoints()
    
    def get_code_memory_view(self):
        return self.code_memory_view
    
    def change_paned_window_appearance(self):
        # TODO para que uso esto
        bg_color = self.get_single_color(self.cget("fg_color"))
        self.paned_memory.configure(bg=bg_color, proxybackground=bg_color, background=bg_color)
        self.code_memory_view.change_appearance_mode()      
    
    def get_single_color(self, color_tuple):
        """Convert CTk color tuple to single color string based on current appearance mode"""
        if ctk.get_appearance_mode() == "Light":
            return color_tuple[0]  
        else:
            return color_tuple[1] 
