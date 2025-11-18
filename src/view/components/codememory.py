import sys
import customtkinter as ctk
from tkinter import ttk
from typing import List, Optional, Callable
from view.components.breakpoint_canvas import BreakpointCanvas
from view.utils.color_manager import ColorManager
from view.utils.time import debounce

class CodeMemoryView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_breakpoint_change: Optional[Callable] = None
        self.on_pc_change: Optional[Callable] = None
        
        self.breakpoints = set()
        self.current_pc = None
        self.codecell_list_length = None
        self.last_executed_instruction = None
        self.tree_items_address_to_treeview_ID = {}
        self._currently_selected_address = None
        
        self.annotations = {}
        self.tooltip_list = []
        self.current_hover_row = None
        self.tooltip_scheduled_id_list = []
        
        self._initialize_column_width_dictionaries()
        self._create_widgets()
        self._setup_styles()
        self._setup_layout()
        self._setup_bindings()
        
    def load_code(self, code_data: List[dict], clear_breakpoints = True):
        """
        Load code into the memory view
        Args:
            code_data: List of dictionaries with keys: 
                    'label', 'address', 'instruction', 'annotation'
            clear_breapoints: True to clear breakpoint list.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if clear_breakpoints:
            self.breakpoints.clear()
        
        self.tree_items_address_to_treeview_ID.clear()
        self.annotations.clear()
        self.codecell_list_length = len(code_data)
        self.current_pc = 0
        self.last_executed_instruction = None

        for i, instruction in enumerate(code_data):
            self._create_tree_item(instruction, i)  
            
        self._auto_size_columns()
        self.after_idle(lambda: self._update_breakpoint_canvas())
        
    def set_current_pc(self, pc_value: int, last_executed_instruction_address: int):
        """
        Set the current program counter by PC value
        Args:
            pc_value: PC value to highlight as current, or None to clear
        """
        old_pc_line = self.current_pc
        old_last_executed_instruction_address = self.last_executed_instruction
        self.last_executed_instruction = last_executed_instruction_address
        
        if pc_value is not None and self.codecell_list_length > 0 and pc_value < self.codecell_list_length:
            self.current_pc = pc_value
        else:
            self.current_pc = None

        addresses_to_update = set()
        if old_pc_line is not None:
            addresses_to_update.add(old_pc_line)
        if self.current_pc is not None:
            addresses_to_update.add(self.current_pc)
        if old_last_executed_instruction_address is not None:
            addresses_to_update.add(old_last_executed_instruction_address)
        if self.last_executed_instruction is not None:
            addresses_to_update.add(self.last_executed_instruction)
        
        for address in addresses_to_update:
            if address in self.tree_items_address_to_treeview_ID:
                self._update_line_appearance(address)
        
        if self.on_pc_change:
            self.on_pc_change(pc_value, self.current_pc)
        
    def reset(self):
        self.after_idle(lambda: self._update_breakpoint_canvas())
        
    def get_selected_address(self):
        return self._currently_selected_address
    
    def _initialize_column_width_dictionaries(self):
        self.column_widths = {
            'breakpoint': 20,
            'pc': 30,
            'label': 80,
            'address': 80,
            'instruction': 200,
        }
        
        self.broader_column_widths = {
            'breakpoint': {'width': 20, 'address': 0},
            'pc': {'width': 30, 'address': 0},
            'label': {'width': 80, 'address': 0},
            'address': {'width': 80, 'address': 0},
            'instruction': {'width': 200, 'address': 0}
        }
        
    def _create_widgets(self):
        """Create all the widgets for the code memory view"""  
        self.style = ttk.Style()
        self.tree_frame = ctk.CTkFrame(self)
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=('pc', 'label', 'address', 'instruction'),
            show='tree headings',
            height=25,
            padding=0,
            selectmode="browse",
        )
        
        canvas_width = self.column_widths['breakpoint']
        self.breakpoint_canvas = BreakpointCanvas(
            self.tree_frame, 
            width=canvas_width, 
            height=400,
            on_breakpoint_click_callback=self._toggle_breakpoint,
            bg=ColorManager.get_theme_background_color(self.master)
        )
        
        self.tree.column('#0', width=0, stretch=False)
        self.tree.column('pc', width=self.column_widths['pc'], anchor='center', stretch=False, minwidth=self.column_widths['pc'])
        self.tree.column('label', width=self.column_widths['label'], anchor='w', stretch=False, minwidth=self.column_widths['label'])
        self.tree.column('address', width=self.column_widths['address'], anchor='w', stretch=False, minwidth=self.column_widths['address'])
        self.tree.column('instruction', width=self.column_widths['instruction'], anchor='w', stretch=False, minwidth=self.column_widths['instruction'])
        
        self.tree.heading('pc', text='PC', anchor='w')
        self.tree.heading('label', text='Label', anchor='w')
        self.tree.heading('address', text='Address', anchor='w')
        self.tree.heading('instruction', text='Instruction', anchor='w')
        
        self.v_scrollbar = ctk.CTkScrollbar(self.tree_frame, orientation="vertical", command=self.tree.yview)
        self.h_scrollbar = ctk.CTkScrollbar(self.tree_frame, orientation="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self._on_tree_vertical_scroll, xscrollcommand=self.h_scrollbar.set)
        
    def _setup_styles(self):
        """Configure ttk styles for the treeview"""
        
        bg_color = ColorManager.get_theme_background_color(self) 
        
        self._define_tree_tag_configurations()
        self.breakpoint_canvas.configure(background=bg_color)
        
        self.tree.update_idletasks()
        
    def _define_tree_tag_configurations(self):
        self.tree.tag_configure('current_pc', background=ColorManager.SECONDARY_COLOR, foreground='white')
        self.tree.tag_configure('last_executed', background=ColorManager.TERTIARY_COLOR, foreground='black')
        self.tree.tag_configure('even', background=ColorManager.get_alternating_colors(self, 0))
        self.tree.tag_configure('odd', background=ColorManager.get_alternating_colors(self, 1))
        self.tree.tag_configure('has_annotation', font=ctk.CTkFont(weight="bold"))
        
    def _setup_layout(self):
        """Set up the layout of the widgets"""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.tree_frame.grid(row=0, column=0, sticky="nsew", padx=(0,5), pady=5)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(1, weight=0)
        self.tree_frame.grid_columnconfigure((0,2), weight=0)
        self.tree_frame.grid_columnconfigure(1,weight=1)
        
        self.breakpoint_canvas.grid(row=0,column=0, rowspan=2, sticky="ns")
        self.tree.grid(row=0, column=1, sticky="nsew")
        self.v_scrollbar.grid(row=0, column=2, sticky="ns")
        self.h_scrollbar.grid(row=1, column=1, sticky="ew")
        
        self.v_scrollbar.grid_remove()
        self.h_scrollbar.grid_remove()
        
    def _setup_bindings(self):
        self.tree_frame.bind('<Configure>', lambda e: self._on_configure(e))
        self.tree.bind("<Shift-MouseWheel>", lambda e: self._on_shift_scroll(event=e))
        self.tree.bind("<Shift-Button-4>", lambda e: self._on_shift_scroll_horizontal(e, -3))
        self.tree.bind("<Shift-Button-5>", lambda e: self._on_shift_scroll_horizontal(e, 3))

        self.tree.bind("<Motion>", self._on_tree_motion)
        self.tree.bind("<Leave>", self._on_tree_leave)
        self.tree.bind("<<TreeviewSelect>>", self._on_selection)
        
        self.tree.bind('<Configure>', lambda e: self._on_configure(e))
        self.bind('<Configure>', lambda e: self._on_configure(e))
        
    def _on_selection(self, event):
        selected_row_item = self.tree.selection()
        if len(selected_row_item) > 0:
            selected_address = self._get_address_from_item(selected_row_item[0])
            if selected_address != self._currently_selected_address:
                self._currently_selected_address = self._get_address_from_item(selected_row_item)
            else:
                self.tree.selection_remove(selected_row_item)
                self._currently_selected_address = None
        
    def _on_tree_vertical_scroll(self, *args):
        self.v_scrollbar.set(*args)
        self.after_idle(lambda: self._update_breakpoint_canvas())
        self._hide_tooltips()
    
    def _on_configure(self, event):
        self._update_scrollbar_visibility()
        self.after_idle(lambda: self._update_breakpoint_canvas())
    
    def _on_shift_scroll(self, event):
        if sys.platform == "darwin":  # macOS
            delta = event.delta 
        else:  # Windows
            delta = int(event.delta / 10)
            
        self.tree.xview_scroll(-delta, "units")
        self.after_idle(lambda: self._update_breakpoint_canvas())
        self.after_idle(lambda: self._on_tree_motion(event))
        return "break"
    
    @debounce(timeout=0.02)
    def _on_tree_motion(self, event):
        """Handle mouse motion in treeview for tooltips"""
        item = self.tree.identify_row(event.y)
        if item:
            column = self.tree.identify_column(event.x)
            instruction_column = '#4'
            if column == instruction_column:
                address = self._get_address_from_item(item)
                if address is not None and address>=0 and address in self.annotations and self.annotations[address]:
                    annotation = self.annotations[address]
                    self._schedule_tooltip(row=item, column=column, annotation=annotation)
                else:
                    self.after_idle(lambda: self._hide_tooltips())
            else:
                self.after_idle(lambda: self._hide_tooltips())
        else:
            self.after_idle(lambda: self._hide_tooltips())
    
    def _on_tree_leave(self, event):
        """Handle mouse leaving treeview"""
        self.after(200, lambda: self._hide_tooltips())
    
    def _on_tree_horizontal_scroll(self, event, units):
        self.tree.xview_scroll(units, "units")
        self.after_idle(lambda: self._update_breakpoint_canvas())
        self.after_idle(lambda: self._on_tree_motion(event))
        
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
            
    def _create_tree_item(self, instruction: dict, index: int):
        """Create a single line widget for an instruction"""
        address = instruction['address']
        label = instruction.get('label', '')
        instruction_text = instruction.get('instruction', '')
        annotation = instruction.get('annotation', '')
        
        if label is not None:
            self._check_column_width(text=f"{label}", column_name='label', address= address)
        
        if instruction_text is not None:
            self._check_column_width(text=str(instruction_text), column_name='instruction', address= address)
            
        if annotation is not None:
            self.annotations[address] = annotation
            
        pc_indicator = ""
        
        item_id = self.tree.insert('', 'end', 
                                  values=(pc_indicator, label, address, instruction_text),
                                  tags=(str(address),))
        
        self.tree_items_address_to_treeview_ID[address] = item_id
        self._update_line_appearance(address)
    
    def _update_line_appearance(self, address: int, color = None):
        """Update the visual appearance of a line based on its state"""       
        if address not in self.tree_items_address_to_treeview_ID:
            return
        
        item_id = self.tree_items_address_to_treeview_ID[address]
        
        # values = (pc, label, address, instruction)
        values = list(self.tree.item(item_id, 'values'))
        
        values[0] = "→" if self._current_pc_on_address(address) else ""
        
        tags = [str(address)]
        if self.last_executed_instruction is not None and address == self.last_executed_instruction:
            tags.append('last_executed')
        elif self._current_pc_on_address(address):
            tags.append('current_pc')
        else:
            self._append_color_tag(address, tags)
        
        if address in self.annotations and self.annotations[address]:
            tags.append('has_annotation')
        
        self.tree.item(item_id, values=values, tags=tags)
        
    def _auto_size_columns(self):
        """Automatically size columns based on content"""
        for column_name in ['label', 'address', 'instruction']:
            if self.tree.column(column_name)['width'] != self.broader_column_widths[column_name]['width']:
                self.tree.column(column_name, width=self.broader_column_widths[column_name]['width'])
                
        self._update_scrollbar_visibility()
            
    def _update_breakpoint_canvas(self):
        if not self.breakpoint_canvas:
            return
            
        self.breakpoint_canvas.clear()
        
        canvas_height = self.tree.winfo_height()
        if canvas_height > 1:  # Only update if treeview has valid height
            self.breakpoint_canvas.configure(height=canvas_height)
        
        for address in self.tree_items_address_to_treeview_ID:
            item_id = self.tree_items_address_to_treeview_ID[address]
            bbox = self.tree.bbox(item_id)
            if bbox:
                x = self.column_widths['breakpoint'] // 2
                y = self._get_y_root_from_item_boundingbox(bbox) + self._get_height_of_item(bbox) // 2
                self.breakpoint_canvas.add_breakpoint(x=x, y=y, address= address, active=address in self.breakpoints)
        
        self.breakpoint_canvas.update_idletasks()
        
    def _toggle_breakpoint(self, address: int):
        """Toggle breakpoint for a specific line"""
        if address in self.breakpoints.copy():
            self.breakpoints.remove(address)
        else:
            self.breakpoints.add(address)
        
        if self.on_breakpoint_change:
            self.on_breakpoint_change()
    
    def _schedule_tooltip(self, row, column, annotation):
        self._clear_tooltip_schedule_list()
        self.tooltip_scheduled_id_list.append(self.after_idle(lambda: self._create_tooltip(row, column, annotation)))
    
    def _create_tooltip(self, row_item, column, annotation):
        """Create a tooltip with the annotation text next to the instruction column"""
        instruction_boundingbox = self.tree.bbox(row_item, column)
        
        if instruction_boundingbox:
            tree_width = self.tree_frame.winfo_width()
            screen_height = self.winfo_screenheight()
            default_scrollbar_width = 16    
            tooltip_height = self.style.configure("Treeview")['rowheight']
            tree_x_root = self.tree.winfo_rootx()
            tree_y_root = self.tree.winfo_rooty()
            
            x = tree_x_root + self._get_x_root_from_item_boundingbox(instruction_boundingbox) + self._get_width_of_item(instruction_boundingbox)
            y = tree_y_root + self._get_y_root_from_item_boundingbox(instruction_boundingbox)
            if len(self.tooltip_list) > 0 and self.current_hover_row != row_item or len(self.tooltip_list) == 0:
                self.current_hover_row = row_item
                tree_x_end = self.tree_frame.winfo_rootx() + tree_width + self.column_widths['breakpoint'] - default_scrollbar_width
                if x > tree_x_end:
                    x = tree_x_end
                 
                if y + tooltip_height > screen_height:
                    y = y - tooltip_height - 5
                
                tooltip = ctk.CTkToplevel(self)
                tooltip.wm_overrideredirect(True)
                tooltip.wm_attributes("-topmost", True)
                tooltip.wm_geometry(f"+{x}+{y}")
                
                tooltip_frame = ctk.CTkFrame(tooltip, corner_radius=5, fg_color=ColorManager.SECONDARY_COLOR)
                tooltip_frame.pack(padx=0, pady=0, fill="both", expand=True)
                
                tooltip_label = ctk.CTkLabel(
                    tooltip_frame, 
                    text=annotation, 
                    height=tooltip_height,
                    wraplength=280,
                    justify="left",
                    fg_color=ColorManager.SECONDARY_COLOR,
                    text_color="white",
                    padx=2,
                    pady=2
                )
                tooltip_label.pack(fill="both", expand=True)
                if len(self.tooltip_list) > 0:
                    self._destroy_tooltips()
                self._clear_tooltip_schedule_list()
                self.tooltip_list.append(tooltip)
      
    def _destroy_tooltips(self):
        tooltip_list_copy = self.tooltip_list.copy()
        self.tooltip_list = []
        for tooltip in tooltip_list_copy:
            tooltip.destroy()
    
    def _hide_tooltips(self):
        self.update_idletasks()
        self._clear_tooltip_schedule_list()
        self._destroy_tooltips()
        self.current_hover_row = None
    
    def _clear_tooltip_schedule_list(self):
        tooltip_id_list_copy = self.tooltip_scheduled_id_list.copy()
        if len(tooltip_id_list_copy) > 0:
            self.tooltip_scheduled_id_list = []
        for tooltip_id in tooltip_id_list_copy:
            self.after_cancel(tooltip_id)
    
    def destroy(self):
        """Override destroy to clean up tooltips"""
        self._hide_tooltips()
        super().destroy()                
    
    def get_breakpoints(self) -> set:
        """Get all currently set breakpoints"""
        return self.breakpoints.copy()
    
    def clear_breakpoints(self):
        """Clear all breakpoints"""
        self.breakpoints.clear()
        self.breakpoint_canvas.clear()
    
    def set_breakpoint_change_callback(self, callback: Callable):
        """
        Set a callback function for breakpoint changes
        Args:
            callback: Function that takes (line_num: int, is_set: bool)
        """
        self.on_breakpoint_change = callback
    
    def change_appearance_mode(self, new_appearance_mode):
        self._setup_styles()

    def _append_color_tag(self, address, tag_list):
        if address % 2 == 0:
            tag_list.append('even')
        else:
            tag_list.append('odd')

    def _current_pc_on_address(self, address: int):
        return True if address == self.current_pc else False

    def _get_address_from_item(self, item):
        """Extract address from treeview item"""
        values = self.tree.item(item, 'values')
        if values and len(values) >= 4:
            address_column_index = 2
            try:
                return int(values[address_column_index])
            except (ValueError, IndexError):
                return None
        return None

    def _check_column_width(self, text, column_name, address):
        text_width = self._calculate_text_width(text)
        if self.broader_column_widths[column_name]['address'] == address and self.column_widths[column_name] < text_width:
            self.broader_column_widths[column_name]['width'] = text_width
        elif self.broader_column_widths[column_name]['width'] < text_width:
            self.broader_column_widths[column_name]['address'] = address
            self.broader_column_widths[column_name]['width'] = text_width

    def _calculate_text_width(self, text):
        """Calculate appropriate width based on text length"""
        font = ctk.CTkFont(weight='bold')
        padding = 10
        return font.measure(text) + padding

    def _get_x_root_from_item_boundingbox(self,bbox):
        return bbox[0]
    
    def _get_y_root_from_item_boundingbox(self, bbox):
        return bbox[1]
    
    def _get_height_of_item(self, bbox):
        return bbox[3]
    
    def _get_width_of_item(self, bbox):
        return bbox[2]