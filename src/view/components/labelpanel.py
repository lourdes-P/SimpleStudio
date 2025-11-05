import customtkinter as ctk
from view.components.dualscrollframe import DualScrollFrame
from typing import List, Dict

class LabelPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, height=150, width=200+35, **kwargs)
        
        self.column_widths = {
            'label': 100,
            'address': 100,
        }
        
        self._create_widgets()
        self._setup_layout()
        
    def _create_widgets(self):
        self.line_widgets: Dict[int, dict] = {}
        self.label_index = {}
        self.line_widget_index = 0
        self.grid_propagate(False)
        
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=22)
        
        self.header_frame.grid_columnconfigure(0, minsize=self.column_widths['label'])
        self.header_frame.grid_columnconfigure(1, minsize=self.column_widths['address'])
        
        self.label_header = ctk.CTkLabel(self.header_frame, text="Label", width=self.column_widths['label'], anchor="w")
        self.address_header = ctk.CTkLabel(self.header_frame, text="Address", width=self.column_widths['address'], anchor="w")

        
        self.scroll_frame = DualScrollFrame(self, height=150, width=200)
        
        self.label_frame =  ctk.CTkFrame(self.scroll_frame.get_scrollable_frame(), fg_color="transparent", height=100, width=100)
        self.label_frame.pack(fill="both", expand=True)
        
    def _setup_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(2, 0))
        self.label_header.grid(row=0, column=0, padx=2, pady=2, sticky="w")
        self.address_header.grid(row=0, column=1, padx=2, pady=2, sticky="w")
        
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))
        
    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
        self.scroll_frame.change_appearance_mode()    
    
    def load_data(self, data: List[dict]):
        """
        Load label information.
        Each label follows the structure:
            name: (label name)
            address: (value)
        """
        for widget in self.label_frame.winfo_children():
            widget.destroy()
        self.line_widgets.clear()
        self.label_index.clear()
        
        for i, label in enumerate(data):
            self._create_line_widget(label, i)
            
    def reset(self, label_list):
        self.load_data(label_list)
            
    def add_label(self, label: dict, color = None):
        self._create_line_widget(label, self.line_widget_index, color)
        
    def add_label_list(self, label_list, color):
        for i, label in enumerate(label_list):
            widget_index = self.label_index.get(label['name'])
            if widget_index is None:
                self.add_label(label, color)
            else:
                self._update_line_widget_address(label, widget_index)
            
    def delete_label(self, label_name):
        index = self.label_index[label_name]
        line_frame = self.line_widgets[index].get('line_frame')
        line_frame.destroy()
    
    def _update_line_widget_address(self, label : dict, index : int):
        label_address = label['address']
        address_label = self.line_widgets[index].get('address_label')
        address_label.configure(text=str(label_address))
        
    def _create_line_widget(self, label: dict, index: int, color = None):
        label_name = label['name']
        label_value = label['address']
        
        line_frame = ctk.CTkFrame(self.label_frame, height=20, corner_radius=0)
        line_frame.pack(fill="x", pady=1)
        
        name_label = ctk.CTkLabel(line_frame, text=str(label_name), 
                                width=self.column_widths['label'], anchor="w", height=20)
        address_label = ctk.CTkLabel(line_frame, text=str(label_value), 
                                width=self.column_widths['address'], anchor="w", height=20)
        
        name_label.grid(row=0, column=0, padx=2, pady=2, sticky="w")
        address_label.grid(row=0, column=1, padx=2, pady=2, sticky="w")
        
        if color is not None:
            line_frame.configure(fg_color=color)
            name_label.configure(text_color="white")
            address_label.configure(text_color="white")
        
        self.line_widgets[index] = {
            'name': label_name,
            'address': label_value,
            'line_frame': line_frame,
            'name_label': name_label,
            'address_label': address_label
        }
        self.label_index[label_name] = index
        
        self.line_widget_index = index + 1
        