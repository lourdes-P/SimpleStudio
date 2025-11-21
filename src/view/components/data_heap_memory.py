import sys
import customtkinter as ctk
from tkinter import ttk
from typing import List
from view.utils.color_manager import ColorManager

class DataHeapMemoryView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.memory_data = []
        self.current_register = None
        self.tree_items = {}  # Map addresses to treeview item IDs
        self.last_modified_cell_address = None
                
        self._initialize_column_width_dictionaries()
        self._create_widgets()
        self._setup_styles()
        self._setup_layout()
        self._setup_bindings()
    
    def reset(self, cell_list):
        """
        Reset modified cells
        Args:
            cell_list: List of dictionaries with keys: 
                    'register', 'address', 'instruction', 'value', 'annotation'
        """
        self.last_modified_cell_address = None
        for cell_data in cell_list:
            address = cell_data.get('address', '')
            register = cell_data.get('register', None)
            value = cell_data.get('value', None)
            annotation = cell_data.get('annotation', None)
            self._update_cell_value(address, value, register, annotation)
            
    def load_memory(self, memory_data: List[dict]):
        """
        Load memory data into the treeview
        Args:
            memory_data: List of dictionaries with keys: 
                    'register', 'address', 'instruction', 'value', 'annotation'
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        self.tree_items.clear()
        self.memory_data = memory_data
        
        for i, cell_data in enumerate(memory_data):
            self._create_tree_item(cell_data, i)
            
        self._auto_size_columns()
        
    def update_memory(self, modified_cells):
        """Update multiple memory cells"""
        last_modified_cell_address = None
        for cell_data in modified_cells:
            address = cell_data.get('address', '')
            register = cell_data.get('register', None)
            value = cell_data.get('value', None)
            annotation = cell_data.get('annotation', None)
            memory_modified = cell_data.get('memory_modified', False)
            
            self._update_cell_value(address, value, register, annotation)
            
            if memory_modified:
                last_modified_cell_address = address
        
        if last_modified_cell_address is not None:
            self._update_last_modified_cell(last_modified_cell_address)
        
        self._auto_size_columns()
            
    def _initialize_column_width_dictionaries(self):
        self.column_widths = {
            'register': 80,
            'address': 80,
            'value': 80,
            'annotation': 150
        }
        
        self.broader_column_widths = {
            'register': { 'width': 80,
                         'address': 0
                        },
            'address': { 'width': 80,
                         'address': 0
                        },
            'value': { 'width': 80,
                         'address': 0
                        },
            'annotation': { 'width': 150,
                         'address': 0
                        }
        }
        
    def _setup_styles(self):
        """Configure ttk styles for the treeview"""
        if not hasattr(self, "style"):
            self.style = ttk.Style()
            self.style.layout("Treeview", [
            ('Treeview.treearea', {'sticky': 'nswe'})
            ])
            
        available_themes = self.style.theme_names()
        if 'clam' in available_themes:
            self.style.theme_use('clam')
        elif 'alt' in available_themes:
            self.style.theme_use('alt')
        else:
            self.style.theme_use(available_themes[0])
        
        font= ctk.CTkFont()
        self.style.configure("Treeview", font=(font.actual("family"), font.actual("size")))
        self.style.configure("Treeview.Heading", font=(font.actual("family"), font.actual("size"), "bold"))

        bg_color_master = ColorManager.get_theme_background_color(self.master)
        bg_color = ColorManager.get_theme_background_color(self)
        text_color = ColorManager.get_theme_text_color()
        self.style.configure("Treeview", 
                           background=bg_color_master,
                           foreground=text_color,
                           fieldbackground=bg_color_master,
                           rowheight=25, 
                           borderwidth=0,
                           highlightthickness=0, 
                           bd=0,
                           indent=0,
                           relief="flat")
        
        self.style.configure("Treeview.Heading",
                           background=bg_color,
                           foreground=text_color,
                           relief="flat",
                           )
        
        self.style.map('Treeview.Heading',
                      background=[('active', bg_color_master),
                                ('pressed', bg_color_master)],
                      relief=[('pressed', 'flat')])
        
        self._define_tree_tag_configurations()

        self.tree.update_idletasks()
        
    def _create_widgets(self):
        """Create all the widgets for the memory view"""
        
        # Create Treeview for memory cells
        self.tree_frame = ctk.CTkFrame(self)
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=('register', 'address', 'value', 'annotation'),
            show='tree headings',  # Hide the first empty column
            height=25,# Show 25 rows by default
            padding=0,
            selectmode="none",
            style='Treeview'
        )
        
        # Configure columns
        self.tree.column('#0', width=0, stretch=False)  # Hide first column
        self.tree.column('register', width=self.column_widths['register'], anchor='w', stretch=False)
        self.tree.column('address', width=self.column_widths['address'], anchor='w', stretch=False)
        self.tree.column('value', width=self.column_widths['value'], anchor='w', stretch=False)
        self.tree.column('annotation', width=self.column_widths['annotation'], anchor='w', stretch=False)
        # Configure headings
        self.tree.heading('register', text='Register', anchor='w')
        self.tree.heading('address', text='Address', anchor='w')
        self.tree.heading('value', text='Value', anchor='w')
        self.tree.heading('annotation', text='Annotation', anchor='w')
        
        self.v_scrollbar = ctk.CTkScrollbar(self.tree_frame, orientation="vertical", command=self.tree.yview)
        self.h_scrollbar = ctk.CTkScrollbar(self.tree_frame, orientation="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        
    def _setup_layout(self):
        """Set up the layout of the widgets"""
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.tree_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(5, 5))
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.v_scrollbar.grid_remove()
        self.h_scrollbar.grid_remove()
        
    def _define_tree_tag_configurations(self):
        self.tree.tag_configure('modified', background=ColorManager.TERTIARY_COLOR, foreground='black')
        self.tree.tag_configure('register', background=ColorManager.SECONDARY_COLOR, foreground='white')
        self.tree.tag_configure('even', background=ColorManager.get_alternating_colors(self, 0))
        self.tree.tag_configure('odd', background=ColorManager.get_alternating_colors(self, 1))
        
    def _setup_bindings(self):
        self.tree_frame.bind('<Configure>', lambda e: self._update_scrollbar_visibility())
        self.tree.bind("<Shift-MouseWheel>", lambda e: self._on_shift_scroll(event=e))
        self.tree.bind("<Shift-Button-4>", lambda e: self.tree.xview_scroll(-3, "units"))
        self.tree.bind("<Shift-Button-5>", lambda e: self.tree.xview_scroll(3, "units"))
        
    def _on_shift_scroll(self, event):
        if sys.platform == "darwin":  # macOS
            delta = event.delta 
        else:  # Windows
            delta = int(event.delta / 20)
            
        self.tree.xview_scroll(-delta, "units")
        
    def _update_scrollbar_visibility(self):
        """Show/hide scrollbars based on content size"""
        self.tree.update_idletasks()
        
        yview = self.tree.yview()
        if yview == (0.0, 1.0):
            self.v_scrollbar.grid_remove()
        else:
            self.v_scrollbar.grid()
        
        xview = self.tree.xview()
        if xview == (0.0, 1.0):  
            self.h_scrollbar.grid_remove()
        else:
            self.h_scrollbar.grid()

    def _auto_size_columns(self):
        """Automatically size columns based on content"""
        if self.tree.column('register')['width'] != self.broader_column_widths['register']['width']:
            self.tree.column('register', width=self.broader_column_widths['register']['width'])
            
        if self.tree.column('value')['width'] != self.broader_column_widths['value']['width']:
            self.tree.column('value', width=self.broader_column_widths['value']['width'])
            
        if self.tree.column('annotation')['width'] != self.broader_column_widths['annotation']['width']:
            self.tree.column('annotation', width=self.broader_column_widths['annotation']['width'])
            
        self._update_scrollbar_visibility()
    
    def _create_tree_item(self, cell_data: dict, index: int):
        """Create a single treeview item for a memory cell"""
        address = cell_data.get('address', '')
        register = cell_data.get('register', '')
        value = cell_data.get('value', '###')
        annotation = cell_data.get('annotation', '')
     
        item_id = self.tree.insert('', 'end', 
                                  values=(register, address, value, annotation),
                                  tags=(address,))
        
        self.tree_items[address] = item_id
        
        self._update_cell_appearance(address)
    
    def _update_cell_appearance(self, address: str):
        """Update the visual appearance of a cell based on its state"""
        if address not in self.tree_items:
            return
        
        row_item_id = self.tree_items[address]
        
        values = self.tree.item(row_item_id, 'values')
        register_text = values[0] if values else ''
        
        row_item_tags = []
        
        if self.last_modified_cell_address is not None and int(self.last_modified_cell_address) == int(address):
            row_item_tags.append('modified')
        elif register_text and register_text.strip():
            row_item_tags.append('register')
        else:
            # Alternate row coloring
            if int(address) % 2 == 0:
                row_item_tags.append('even')
            else:
                row_item_tags.append('odd')
        
        self.tree.item(row_item_id, tags=row_item_tags)
    
    def _update_cell_value(self, address: str, value: str = None, register: str = None, annotation: str = None):
        """Update the value of a specific memory cell"""
        if address not in self.tree_items:
            return
        
        item_id = self.tree_items[address]
        current_values = list(self.tree.item(item_id, 'values'))
        
        updated = False
        if value is not None and current_values[2] != value:
            self._check_column_width(text=f"{value}", column_name='value', address= address)
            current_values[2] = value
            updated = True
        
        if register is not None and current_values[0] != register:
            self._check_column_width(text=str(register), column_name='register', address= address)
            current_values[0] = register
            updated = True
            
        if annotation is not None and current_values[3] != annotation:
            self._check_column_width(text=str(annotation), column_name='annotation', address= address)
            current_values[3] = annotation
            updated = True
        
        if updated:
            self.tree.item(item_id, values=current_values)
            
            # Update data model
            for cell in self.memory_data:
                if cell.get('address') == address:
                    if value is not None:
                        cell['value'] = value
                    if register is not None:
                        cell['register'] = register
                    if annotation is not None:
                        cell['annotation'] = annotation
                    break
            
        self._update_cell_appearance(address)
    
    def _update_last_modified_cell(self, last_modified_cell_address):
        """Update the last modified cell highlight"""
        former_last_modified_cell_address = self.last_modified_cell_address
        self.last_modified_cell_address = last_modified_cell_address
        
        if former_last_modified_cell_address is not None:
            self._update_cell_appearance(former_last_modified_cell_address)
        if self.last_modified_cell_address is not None:
            self._update_cell_appearance(self.last_modified_cell_address)
    
    def _check_column_width(self, text, column_name, address):
        text_width = self._calculate_text_width(text)
        if self.broader_column_widths[column_name]['address'] == address and self.column_widths[column_name] < text_width:
            self.broader_column_widths[column_name]['width'] = text_width
        elif self.broader_column_widths[column_name]['width'] < text_width:
            self.broader_column_widths[column_name]['address'] = address
            self.broader_column_widths[column_name]['width'] = text_width

    def _calculate_text_width(self, text):
        """Calculate appropriate width based on text length"""
        font = ctk.CTkFont()
        padding = 20
        return font.measure(text) + padding
    
    def change_appearance_mode(self, new_appearance_mode):
        """Update appearance based on the selected mode"""
        self._setup_styles()