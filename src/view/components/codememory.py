import customtkinter as ctk
from customtkinter import ThemeManager
from typing import List, Dict, Optional, Callable

class CodeMemoryView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Configuration
        self.breakpoints = set()
        self.current_pc = None
        self.on_breakpoint_change: Optional[Callable] = None
        self.on_pc_change: Optional[Callable] = None
        self.default_text_color = None
        self.codecell_list = None
        
        # Create the main layout
        self._create_widgets()
        self._setup_layout()
        self.set_current_pc_by_line(1)
        
    def _create_widgets(self):
        """Create all the widgets for the code memory view"""
        # Header frame
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        # Column headers 
        self.pc_header = ctk.CTkLabel(self.header_frame, text="PC", width=40, anchor="w")
        self.label_header = ctk.CTkLabel(self.header_frame, text="Label", width=80, anchor="w")
        self.line_header = ctk.CTkLabel(self.header_frame, text="Line", width=80, anchor="w")
        self.instruction_header = ctk.CTkLabel(self.header_frame, text="Instruction", width=200, anchor="w")
        self.annotation_header = ctk.CTkLabel(self.header_frame, text="Annotation", width=150, anchor="w")
        
        # Scrollable frame for code lines
        self.scroll_frame = ctk.CTkScrollableFrame(self, height=400)
        self.code_lines_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.code_lines_frame.pack(fill="both", expand=True)
        
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
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 0))
        self.pc_header.grid(row=0, column=0, padx=2, pady=2, sticky="w")
        self.label_header.grid(row=0, column=1, padx=2, pady=2, sticky="w")
        self.line_header.grid(row=0, column=2, padx=2, pady=2, sticky="w")
        self.instruction_header.grid(row=0, column=3, padx=2, pady=2, sticky="w")
        self.annotation_header.grid(row=0, column=4, padx=2, pady=2, sticky="w")   
        
        # Scroll frame layout
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
    def load_code(self, code_data: List[dict]):
        """
        Load code into the memory view
        
        Args:
            code_data: List of dictionaries with keys: 
                    'label', 'line', 'instruction', 'annotation'
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
        line_num = instruction['line']
        
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
        line_label = ctk.CTkLabel(line_frame, text=str(line_num), 
                                 width=80, anchor="w")
        instruction_label = ctk.CTkLabel(line_frame, text=str(instruction.get('instruction', '')), 
                                        width=200, anchor="w")
        annotation_label = ctk.CTkLabel(line_frame, text=str(instruction.get('annotation', '')), 
                                        width=150, anchor="w")
        
        # Layout widgets
        label_label.grid(row=0, column=1, padx=2, pady=2, sticky="w")
        line_label.grid(row=0, column=2, padx=2, pady=2, sticky="w")
        instruction_label.grid(row=0, column=3, padx=2, pady=2, sticky="w")
        annotation_label.grid(row=0, column=4, padx=2, pady=2, sticky="w")
        
        # Make the line clickable for breakpoints
        line_frame.bind("<Button-1>", lambda e, ln=line_num: self._toggle_breakpoint(ln))
        for widget in [pc_frame, label_label, line_label, instruction_label, annotation_label]:
            widget.bind("<Button-1>", lambda e, ln=line_num: self._toggle_breakpoint(ln))
        
        # Store reference to widgets
        self.line_widgets[line_num] = {
            'frame': line_frame,
            'pc_frame': pc_frame,
            'pc_arrow': pc_arrow,
            'label': label_label,
            'line': line_label,
            'instruction': instruction_label,
            'annotation': annotation_label
        }
        
        # Set initial appearance
        self._update_line_appearance(line_num)
    
    def _toggle_breakpoint(self, line_num: int):
        """Toggle breakpoint for a specific line"""
        if line_num in self.breakpoints:
            self.breakpoints.remove(line_num)
        else:
            self.breakpoints.add(line_num)
        
        # Update appearance
        self._update_line_appearance(line_num)
        
        # Notify callback if set
        if self.on_breakpoint_change:
            self.on_breakpoint_change(line_num, line_num in self.breakpoints)
    
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
        label_widgets = ['pc_arrow', 'label', 'line', 'instruction', 'annotation']
                
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
        if self.current_pc_on_line(line_num):
            frame.configure(fg_color="#2c3e50")  # Dark blue background for current PC
            pc_arrow.configure(text="→", text_color="#4ecdc4", font=ctk.CTkFont(weight="bold", size=14))
            for widget_key in label_widgets:
                if widget_key in widgets and hasattr(widgets[widget_key], 'configure'):
                    widgets[widget_key].configure(text_color="white")
    
    def set_current_pc(self, pc_value: Optional[int]):
        """
        Set the current program counter by PC value
        
        Args:
            pc_value: PC value to highlight as current, or None to clear
        """
        old_pc_line = self.current_pc + 1
        
        # Find the line number for this PC value
        if pc_value is not None and self.codecell_list is not None and pc_value < len(self.codecell_list):
            self.current_pc = pc_value
        else:
            self.current_pc = None
        
        # Update appearance of old and new PC lines
        if old_pc_line is not None and old_pc_line in self.line_widgets:
            self._update_line_appearance(old_pc_line)
        if self.current_pc is not None and self.current_pc in self.line_widgets:
            self._update_line_appearance(self.current_pc + 1)
        
        # Notify callback if set
        if self.on_pc_change:
            self.on_pc_change(pc_value, self.current_pc)
    
    def set_current_pc_by_line(self, line_num: Optional[int]):
        """
        Set the current program counter by line number
        
        Args:
            line_num: Line number to highlight as current, or None to clear
        """
        old_pc_line = self.current_pc
        self.current_pc = line_num
        
        # Update appearance of old and new PC lines
        if old_pc_line is not None and old_pc_line in self.line_widgets:
            self._update_line_appearance(old_pc_line)
        if line_num is not None and line_num in self.line_widgets:
            self._update_line_appearance(line_num)
        
        # Get PC value for callback
        pc_value = None
        if line_num is not None and line_num in self.line_to_pc:
            pc_value = self.line_to_pc[line_num]
        
        # Notify callback if set
        if self.on_pc_change:
            self.on_pc_change(pc_value, line_num)
    
    def get_current_pc_value(self) -> Optional[int]:
        """Get the current PC value (None if no PC is set)"""
        if self.current_pc is not None and self.current_pc in self.line_to_pc:
            return self.line_to_pc[self.current_pc]
        return None
    
    def get_current_line(self) -> Optional[int]:
        """Get the current line number (None if no PC is set)"""
        return self.current_pc
    
    def get_breakpoints(self) -> set:
        """Get all currently set breakpoints"""
        return self.breakpoints.copy()
    
    def get_breakpoint_pcs(self) -> set:
        """Get all PC values where breakpoints are set"""
        breakpoint_pcs = set()
        for line_num in self.breakpoints:
            if line_num in self.line_to_pc:
                breakpoint_pcs.add(self.line_to_pc[line_num])
        return breakpoint_pcs
    
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
    
    def get_pc_for_line(self, line_num: int) -> Optional[int]:
        """Get the PC value for a given line number"""
        return self.line_to_pc.get(line_num)
    
    def get_line_for_pc(self, pc_value: int) -> Optional[int]:
        """Get the line number for a given PC value"""
        return self.pc_to_line.get(pc_value)
    
    def current_pc_on_line(self, line: int):
        return True if line == self.current_pc + 1 else False

    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
        temp_label = ctk.CTkLabel(self)
        self.default_text_color = temp_label.cget("text_color")
        temp_label.destroy()