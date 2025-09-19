import customtkinter as ctk
from typing import List, Dict, Optional, Callable
from view.components.dualscrollframe import DualScrollFrame

class DataHeapMemoryView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.memory_data = []
        self.current_register = None
        self.default_text_color = None
        
        self.column_widths = {
            'register': 80,
            'address': 80,
            'value': 80,
            'annotation': 150
        }
        
        self._create_widgets()
        self._setup_layout()
        
    def _create_widgets(self):
        """Create all the widgets for the memory view"""
        # Header frame
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        # Configure header frame grid
        self.header_frame.grid_columnconfigure(0, minsize=self.column_widths['register'])
        self.header_frame.grid_columnconfigure(1, minsize=self.column_widths['address'])
        self.header_frame.grid_columnconfigure(2, minsize=self.column_widths['value'])
        self.header_frame.grid_columnconfigure(3, minsize=self.column_widths['annotation'])
        
        # Column headers 
        self.register_header = ctk.CTkLabel(self.header_frame, text="Register", 
                                           width=self.column_widths['register'], anchor="w")
        self.address_header = ctk.CTkLabel(self.header_frame, text="Address", 
                                          width=self.column_widths['address'], anchor="w")
        self.value_header = ctk.CTkLabel(self.header_frame, text="Value", 
                                        width=self.column_widths['value'], anchor="w")
        self.annotation_header = ctk.CTkLabel(self.header_frame, text="Annotation", 
                                             width=self.column_widths['annotation'], anchor="w")
        
        # Scrollable frame for memory cells
        self.scroll_frame = DualScrollFrame(self)
        self.memory_cells_frame = ctk.CTkFrame(self.scroll_frame.get_scrollable_frame(), fg_color="transparent")
        self.memory_cells_frame.pack(fill="both", expand=True)
        
    def _setup_layout(self):
        """Set up the layout of the widgets"""
        # Configure grid weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Header layout
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(2, 0))
        self.register_header.grid(row=0, column=0, padx=2, pady=2, sticky="w")
        self.address_header.grid(row=0, column=1, padx=2, pady=2, sticky="w")
        self.value_header.grid(row=0, column=2, padx=2, pady=2, sticky="w")
        self.annotation_header.grid(row=0, column=3, padx=2, pady=2, sticky="w")
        
        # Scroll frame layout
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))
        
    def load_memory(self, memory_data: List[dict]):
        """
        Load memory data into the view
        
        Args:
            memory_data: List of dictionaries with keys: 
                    'register', 'address', 'value', 'annotation'
        """
        # Clear existing widgets
        for widget in self.memory_cells_frame.winfo_children():
            widget.destroy()
        self.cell_widgets.clear()
        
        self.memory_data = memory_data
        
        # Create new cell widgets
        for i, cell_data in enumerate(memory_data):
            self._create_cell_widget(cell_data, i)
    
    def _create_cell_widget(self, cell_data: dict, index: int):
        """Create a single cell widget for a memory cell"""
        address = cell_data.get('address', '')
        register = cell_data.get('register', '')
        value = cell_data.get('value', '')
        annotation = cell_data.get('annotation', '')
        
        # Create frame for the cell
        cell_frame = ctk.CTkFrame(self.memory_cells_frame, height=30)
        cell_frame.pack(fill="x", pady=1)
        
        # Create labels for each column
        register_label = ctk.CTkLabel(cell_frame, text=register, 
                                     width=self.column_widths['register'], anchor="w")
        address_label = ctk.CTkLabel(cell_frame, text=address, 
                                    width=self.column_widths['address'], anchor="w")
        value_label = ctk.CTkLabel(cell_frame, text=value, 
                                  width=self.column_widths['value'], anchor="w")
        annotation_label = ctk.CTkLabel(cell_frame, text=annotation, 
                                       width=self.column_widths['annotation'], anchor="w")
        
        # Layout widgets
        register_label.grid(row=0, column=0, padx=2, pady=2, sticky="w")
        address_label.grid(row=0, column=1, padx=2, pady=2, sticky="w")
        value_label.grid(row=0, column=2, padx=2, pady=2, sticky="w")
        annotation_label.grid(row=0, column=3, padx=2, pady=2, sticky="w")
        
        # Store reference to widgets
        self.cell_widgets[address] = {
            'frame': cell_frame,
            'register': register_label,
            'address': address_label,
            'value': value_label,
            'annotation': annotation_label
        }
        
        # Set initial appearance
        self._update_cell_appearance(address)
    
    def _update_cell_appearance(self, address: str):
        """Update the visual appearance of a cell based on its state"""        
        if address not in self.cell_widgets:
            return        
        
        widgets = self.cell_widgets[address]
        frame = widgets['frame']
        
        # Reset colors
        frame.configure(fg_color="transparent")
        
        # Reset text colors for all label widgets
        label_widgets = ['register', 'address', 'value', 'annotation']
                
        for widget_key in label_widgets:
            if widget_key in widgets and hasattr(widgets[widget_key], 'configure'):
                widgets[widget_key].configure(text_color=self.default_text_color)
        
        # Apply register highlighting if this cell has a register
        register_text = widgets['register'].cget('text')
        if register_text and register_text.strip():
            frame.configure(fg_color="#4ecdc4")  # Teal background for register cells
            for widget_key in label_widgets:
                if widget_key in widgets and hasattr(widgets[widget_key], 'configure'):
                    widgets[widget_key].configure(text_color="black")
    
    def update_cell_value(self, address: str, value: str, register: str = None, annotation: str = None):
        """Update the value of a specific memory cell"""
        if address not in self.cell_widgets:
            return
        
        widgets = self.cell_widgets[address]
        
        # Update value
        widgets['value'].configure(text=value)
        
        # Update register if provided
        if register is not None:
            widgets['register'].configure(text=register)
        
        # Update annotation if provided
        if annotation is not None:
            widgets['annotation'].configure(text=annotation)
        
        # Update appearance
        self._update_cell_appearance(address)
        
        # Update the data model
        for cell in self.memory_data:
            if cell.get('address') == address:
                cell['value'] = value
                if register is not None:
                    cell['register'] = register
                if annotation is not None:
                    cell['annotation'] = annotation
                break
    
    def highlight_cell(self, address: str, register: str = None):
        """Highlight a specific memory cell by address"""
        # First, clear any previous highlights
        for addr, widgets in self.cell_widgets.items():
            widgets['frame'].configure(fg_color="transparent")
            for widget_key in ['register', 'address', 'value', 'annotation']:
                if widget_key in widgets:
                    widgets[widget_key].configure(text_color=self.default_text_color)
        
        # Highlight the cell with the matching address
        if address in self.cell_widgets:
            widgets = self.cell_widgets[address]
            widgets['frame'].configure(fg_color="#2c3e50")  # Dark blue background for highlighted cell
            
            # Update text colors for better contrast
            for widget_key in ['register', 'address', 'value', 'annotation']:
                if widget_key in widgets:
                    widgets[widget_key].configure(text_color="white")
            
            # Update register information if provided
            if register is not None:
                widgets['register'].configure(text=register)
                # Update the data model
                for cell in self.memory_data:
                    if cell.get('address') == address:
                        cell['register'] = register
                        break
    
    def change_appearance_mode(self, new_appearance_mode):
        """Update appearance based on the selected mode"""
        ctk.set_appearance_mode(new_appearance_mode)
        
        # Get the default text color for the current mode
        temp_label = ctk.CTkLabel(self)
        self.default_text_color = temp_label.cget("text_color")
        temp_label.destroy()
        
        # Update all cells
        for address in self.cell_widgets.keys():
            self._update_cell_appearance(address)