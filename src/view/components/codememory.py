import customtkinter as ctk
from customtkinter import ThemeManager
from typing import List, Dict, Optional, Callable

from view.components.dualscrollframe import DualScrollFrame

class CodeMemoryView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.breakpoints = set()
        self.current_pc = None
        self.on_breakpoint_change: Optional[Callable] = None
        self.on_pc_change: Optional[Callable] = None
        self.default_text_color = None
        self.codecell_list = None
        
        # for annotations
        self.tooltip = None
        self.current_hover_line = None
        self.tooltip_scheduled_id = None
        
        self.column_widths = {
            'pc': 40,
            'label': 80,
            'line': 80,
            'instruction': 200,
        }
        
        self._create_widgets()
        self._setup_layout()
        
    def _create_widgets(self):
        """Create all the widgets for the code memory view"""  
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        self.header_frame.grid_columnconfigure(0, minsize=self.column_widths['pc'])
        self.header_frame.grid_columnconfigure(1, minsize=self.column_widths['label'])
        self.header_frame.grid_columnconfigure(2, minsize=self.column_widths['line'])
        self.header_frame.grid_columnconfigure(3, minsize=self.column_widths['instruction'])
        
        # Column headers 
        self.pc_header = ctk.CTkLabel(self.header_frame, text="PC", width=self.column_widths['pc'], anchor="w")
        self.label_header = ctk.CTkLabel(self.header_frame, text="Label", width=self.column_widths['label'], anchor="w")
        self.line_header = ctk.CTkLabel(self.header_frame, text="Line", width=self.column_widths['line'], anchor="w")
        self.instruction_header = ctk.CTkLabel(self.header_frame, text="Instruction", width=self.column_widths['instruction'], anchor="w")
        
        # Scrollable frame for code lines
        self.scroll_frame = DualScrollFrame(self)
        
        """self.scroll_frame.grid(row=1,column=0,pady=0)
        v_scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.scroll_frame._parent_canvas.yview) 
        v_scrollbar.grid(row=1, column=1) 
        self.scroll_frame._parent_canvas.configure(yscrollcommand=v_scrollbar.set)"""
        self.code_lines_frame = ctk.CTkFrame(self.scroll_frame.get_scrollable_frame(), fg_color="transparent")
        self.code_lines_frame.pack(fill="both", expand=True)
        # since we clearly need a workaround to have two scroll bars:
        """The workaround is to use the .grid and add a vertical Scrollbar using CTkScrollbar, so: 

        my_frame = customtkinter.CTkScrollableFrame(master=root, orientation="horizontal")
        my_frame.grid(row=1, column=0, pady=10) 

        v_scrollbar = customtkinter.CTkScrollbar(master=root, orientation="vertical", command=my_frame.yview) 
        v_scrollbar.grid(row=1, column=1) 

        my_frame.configure(yscrollcommand=v_scrollbar.set) 

This seemed to work for me for what I was doing with putting a table into the Scrollable Frame and having it scroll through the table. For me, instead of it scrolling the frame, I had it scroll the table instead. """
        
        # Dictionary to store line widgets and PC mapping
        self.line_widgets: Dict[int, dict] = {}  # key: line number
        self.pc_to_line: Dict[int, int] = {}     # key: PC value, value: line number
        self.line_to_pc: Dict[int, int] = {}     # key: line number, value: PC value
        
    def _setup_layout(self):
        """Set up the layout of the widgets"""
        # Configure grid weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Header layout
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(2, 0))
        self.pc_header.grid(row=0, column=0, padx=2, pady=2, sticky="w")
        self.label_header.grid(row=0, column=1, padx=2, pady=2, sticky="w")
        self.line_header.grid(row=0, column=2, padx=2, pady=2, sticky="w")
        self.instruction_header.grid(row=0, column=3, padx=2, pady=2, sticky="w")
        
        # Scroll frame layout
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))
        
    def _create_tooltip(self, text, widget):
        """Create a tooltip with the annotation text"""
        if self.tooltip:
            self.tooltip.destroy()
        
        self.tooltip = ctk.CTkToplevel(self)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_attributes("-topmost", True)
        
        # Get widget position (assign to right of instruction)
        x = widget.winfo_rootx() + widget.winfo_width()
        y = widget.winfo_rooty() 
        
        # Ensure tooltip stays on screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Adjust if tooltip would go off screen right
        tooltip_width = 300
        if x + tooltip_width > screen_width:
            x = screen_width - tooltip_width - 10
        
        # Adjust if tooltip would go off screen bottom
        tooltip_height = 100  # Estimated height
        if y + tooltip_height > screen_height:
            y = widget.winfo_rooty() - tooltip_height - 5
        
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        # Create tooltip content
        tooltip_frame = ctk.CTkFrame(self.tooltip, corner_radius=5, fg_color="#2c3e50")
        tooltip_frame.pack(padx=0, pady=0, fill="both", expand=True)
        
        tooltip_label = ctk.CTkLabel(
            tooltip_frame, 
            text=text, 
            wraplength=280,
            justify="left",
            fg_color="#2c3e50",
            text_color="white",
            padx=2,
            pady=2
        )
        tooltip_label.pack(fill="both", expand=True)
    
    def _hide_tooltip(self):
        """Hide the tooltip"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
        self.current_hover_line = None
        
        # Cancel any scheduled tooltip show
        if self.tooltip_scheduled_id:
            self.after_cancel(self.tooltip_scheduled_id)
            self.tooltip_scheduled_id = None
    
    def _schedule_tooltip(self, widget, annotation):
        """Schedule tooltip to appear after delay"""
        self.tooltip_scheduled_id = self.after(100, lambda: self._create_tooltip(annotation, widget))
        
    def load_code(self, code_data: List[dict]):
        """
        Load code into the memory view
        
        Args:
            code_data: List of dictionaries with keys: 
                    'label', 'address', 'instruction', 'annotation'
        """
        # Clear existing widgets and mappings
        for widget in self.code_lines_frame.winfo_children():
            widget.destroy()
        self.line_widgets.clear()
        self.pc_to_line.clear()
        self.line_to_pc.clear()
        
        self.codecell_list = code_data
        self.current_pc = 0
        
        # Create new line widgets
        for i, instruction in enumerate(code_data):
            self._create_line_widget(instruction, i)
    
    def _create_line_widget(self, instruction: dict, index: int):
        """Create a single line widget for an instruction"""
        line_num = instruction['address']
        annotation = instruction.get('annotation', '')
        
        # Create frame for the line
        line_frame = ctk.CTkFrame(self.code_lines_frame, height=30)
        line_frame.pack(fill="x", pady=1)
        
        # Create PC column with only arrow indicator (no PC value displayed)
        pc_frame = ctk.CTkFrame(line_frame, width=30, height=30, fg_color="transparent")
        pc_frame.pack_propagate(False)  # Prevent children from resizing the frame
        
        pc_arrow = ctk.CTkLabel(pc_frame, text="", width=30, anchor="center")
        pc_arrow.pack(fill="both", expand=True)
        
        pc_frame.grid(row=0, column=0, padx=2, pady=2, sticky="w")
        
        # Create other labels
        label_label = ctk.CTkLabel(line_frame, text=str(instruction.get('label', '')), 
                                  width=80, anchor="w")
        address_label = ctk.CTkLabel(line_frame, text=str(line_num), 
                                 width=80, anchor="w")
        instruction_label = ctk.CTkLabel(line_frame, text=str(instruction.get('instruction', '')), 
                                        width=200, anchor="w")
        
        # Layout widgets
        label_label.grid(row=0, column=1, padx=2, pady=2, sticky="w")
        address_label.grid(row=0, column=2, padx=2, pady=2, sticky="w")
        instruction_label.grid(row=0, column=3, padx=2, pady=2, sticky="w")
        
        # Make the line clickable for breakpoints
        line_frame.bind("<Button-1>", lambda e, ln=line_num: self._toggle_breakpoint(ln))
        for widget in [pc_frame, label_label, address_label, instruction_label]:
            widget.bind("<Button-1>", lambda e, ln=line_num: self._toggle_breakpoint(ln))
        
        # Add hover events for instruction column to show annotation tooltip
        if annotation:  # Only add hover events if there's an annotation
            instruction_label.bind("<Enter>", lambda e, ln=line_num, ann=annotation: self._on_instruction_hover(e, ln, ann, instruction_label))
            instruction_label.bind("<Leave>", lambda e: self._on_instruction_leave(e))
        
        # Store reference to widgets
        self.line_widgets[line_num] = {
            'frame': line_frame,
            'pc_frame': pc_frame,
            'pc_arrow': pc_arrow,
            'label': label_label,
            'address': address_label,
            'instruction': instruction_label,
            'has_annotation': bool(annotation)
        }
        
        # Set initial appearance
        self._update_line_appearance(line_num)
    
    def _on_instruction_hover(self, event, line_num, annotation, widget):
        """Handle mouse entering instruction column"""
        self.current_hover_line = line_num
        self._schedule_tooltip(widget, annotation)
    
    def _on_instruction_leave(self, event):
        """Handle mouse leaving instruction column"""
        self._hide_tooltip()
    
    def _toggle_breakpoint(self, address: int):
        """Toggle breakpoint for a specific line"""
        if address in self.breakpoints:
            self.breakpoints.remove(address)
        else:
            self.breakpoints.add(address)
        
        # Update appearance
        self._update_line_appearance(address)
        
        # Notify callback if set
        if self.on_breakpoint_change:
            self.on_breakpoint_change(address, address in self.breakpoints)
    
    def _update_line_appearance(self, line_num: int):
        """Update the visual appearance of a line based on its state"""        
        if line_num not in self.line_widgets:
            return        
        
        widgets = self.line_widgets[line_num]
        frame = widgets['frame']
        pc_arrow = widgets['pc_arrow']
        
        # Reset colors and arrow
        frame.configure(fg_color="transparent")
        pc_arrow.configure(text="")
        
        # Reset text colors for all label widgets
        label_widgets = ['pc_arrow', 'label', 'address', 'instruction']
                
        for widget_key in label_widgets:
            if widget_key in widgets and hasattr(widgets[widget_key], 'configure'):
                widgets[widget_key].configure(text_color=self.default_text_color)
        
        # Apply breakpoint styling
        if line_num in self.breakpoints:
            frame.configure(fg_color="#ff6b6b")  # Red background for breakpoints
            for widget_key in label_widgets:
                if widget_key in widgets and hasattr(widgets[widget_key], 'configure'):
                    widgets[widget_key].configure(text_color="black")
        
        # Apply current PC styling with arrow
        if self.current_pc_on_address(line_num):
            frame.configure(fg_color="#2c3e50")  # Dark blue background for current PC
            pc_arrow.configure(text="→", text_color="#4ecdc4", font=ctk.CTkFont(weight="bold", size=14))
            for widget_key in label_widgets:
                if widget_key in widgets and hasattr(widgets[widget_key], 'configure'):
                    widgets[widget_key].configure(text_color="white")
        
        # Add subtle indicator for lines with annotations
        if widgets['has_annotation']:
            widgets['instruction'].configure(
                font=ctk.CTkFont(weight="bold")
            )
    
    # Make sure to clean up when the widget is destroyed
    def destroy(self):
        """Override destroy to clean up tooltips"""
        self._hide_tooltip()
        super().destroy()            
    
    def set_current_pc(self, pc_value: Optional[int]):
        """
        Set the current program counter by PC value
        
        Args:
            pc_value: PC value to highlight as current, or None to clear
        """
        old_pc_line = self.current_pc
        
        # Find the line number for this PC value
        if pc_value is not None and self.codecell_list is not None and pc_value < len(self.codecell_list):
            self.current_pc = pc_value
        else:
            self.current_pc = None
        
        # Update appearance of old and new PC lines
        if old_pc_line is not None and old_pc_line in self.line_widgets:
            self._update_line_appearance(old_pc_line)
        if self.current_pc is not None and self.current_pc in self.line_widgets:
            self._update_line_appearance(self.current_pc)
        
        # Notify callback if set
        if self.on_pc_change:
            self.on_pc_change(pc_value, self.current_pc)
    
    def get_current_pc_value(self):
        return self.current_pc
    
    def get_breakpoints(self) -> set:
        """Get all currently set breakpoints"""
        return self.breakpoints.copy()
    
    def clear_breakpoints(self):
        """Clear all breakpoints"""
        breakpoints_copy = self.breakpoints.copy()
        self.breakpoints.clear()
        
        # Update appearance of all lines that had breakpoints
        for line_num in breakpoints_copy:
            if line_num in self.line_widgets:
                self._update_line_appearance(line_num)
        
        # Notify callback if set
        if self.on_breakpoint_change:
            for line_num in breakpoints_copy:
                self.on_breakpoint_change(line_num, False)
    
    def set_breakpoint_change_callback(self, callback: Callable):
        """
        Set a callback function for breakpoint changes
        
        Args:
            callback: Function that takes (line_num: int, is_set: bool)
        """
        self.on_breakpoint_change = callback
    
    def set_pc_change_callback(self, callback: Callable):
        """
        Set a callback function for PC changes
        
        Args:
            callback: Function that takes (pc_value: int, line_num: int)
        """
        self.on_pc_change = callback
    
    def current_pc_on_address(self, address: int):
        return True if address == self.current_pc else False

    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
        temp_label = ctk.CTkLabel(self)
        self.default_text_color = temp_label.cget("text_color")
        temp_label.destroy()
        self.scroll_frame.change_appearance_mode()