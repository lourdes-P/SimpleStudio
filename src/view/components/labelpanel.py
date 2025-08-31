import customtkinter as ctk
from tkinter import ttk

class LabelPanel(ctk.CTkFrame):
    """Component for displaying the label table"""
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
        self.tree = ttk.Treeview(self, columns=self.columns, show='headings', height=5)
        
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
        
        # Insert new data
        for item in new_data:
            self.tree.insert('', 'end', values=item)