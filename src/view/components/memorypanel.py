import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from view.components.codememory import CodeMemoryView
from view.components.data_heap_memory import DataHeapMemoryView

class MemoryPanel(ctk.CTkFrame):
    """Component for displaying memory tables (C, D, or H)"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.paned_memory = None
        
        self.code_memory_view = None
        self.data_memory_view = None
        self.heap_memory_view = None
        
    def initialize(self):
        """self.grid_rowconfigure(1, weight=1)  # Make the code memory expand
        self.grid_columnconfigure((0,1,2), weight=1)"""
        fg_color=self.get_single_color(self.cget("fg_color"))
        self.paned_memory = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.FLAT, bg=fg_color,
                                      borderwidth=0, sashwidth=8, showhandle=False)
        self.paned_memory.pack(fill="both", expand=True)
                        
        self.create_c_memory()
        self.create_d_memory()
        self.create_h_memory()
        
    def create_c_memory(self):     
        self.cmem_container = ctk.CTkFrame(self.paned_memory, corner_radius=0)
        self.cmem_container.grid_rowconfigure(1, weight=1)
        self.cmem_container.grid_columnconfigure(0, weight=1)
        
        cmem_label = ctk.CTkLabel(self.cmem_container, text="C", font=ctk.CTkFont(weight="bold"))
        cmem_label.grid(row=0, column=0, padx=2, pady=(1,0), sticky="sw")
        self.code_memory_view = CodeMemoryView(self.cmem_container)
        self.code_memory_view.grid(row=1, column=0, padx=(0,0), pady=1, sticky="nsew")
        
        self.code_memory_view.set_breakpoint_change_callback(self.on_breakpoint_change)
        self.code_memory_view.change_appearance_mode("System")
        
        self.paned_memory.add(self.cmem_container)
     
    def create_d_memory(self):
        self.dmem_container = ctk.CTkFrame(self.paned_memory, corner_radius=0)
        self.dmem_container.grid_rowconfigure(1, weight=1)
        self.dmem_container.grid_columnconfigure(0, weight=1)
        
        dmem_label = ctk.CTkLabel(self.dmem_container, text="D", font=ctk.CTkFont(weight="bold"))
        dmem_label.grid(row=0, column=0, padx=2, pady=(1,0), sticky="sw")
        self.data_memory_view = DataHeapMemoryView(self.dmem_container)
        self.data_memory_view.grid(row=1, column=0, padx=(0,0), pady=1, sticky="nsew")
        self.data_memory_view.change_appearance_mode("System")

        self.paned_memory.add(self.dmem_container)
        #self.code_memory_view.change_appearance_mode("System")
    
    def create_h_memory(self):
        self.hmem_container = ctk.CTkFrame(self.paned_memory, corner_radius=0)
        self.hmem_container.grid_rowconfigure(1, weight=1)
        self.hmem_container.grid_columnconfigure(0, weight=1)
        
        hmem_label = ctk.CTkLabel(self.hmem_container, text="H", font=ctk.CTkFont(weight="bold"))
        hmem_label.grid(row=0, column=0, padx=2, pady=(1,0), sticky="sw")
        self.heap_memory_view = DataHeapMemoryView(self.hmem_container)
        self.heap_memory_view.grid(row=1, column=0, padx=0, pady=1, sticky="nsew")
        self.heap_memory_view.change_appearance_mode("System")
        
        self.paned_memory.add(self.hmem_container)
        
    def reset(self, parsed_data_memory, parsed_heap_memory):
        self.data_memory_view.reset(parsed_data_memory)
        self.heap_memory_view.reset(parsed_heap_memory)
        
    def load_code_onto_c_memory(self, code_data):
        self.code_memory_view.load_code(code_data)
        
    def load_data_memory(self, data):
        self.data_memory_view.load_memory(data)
        
    def load_heap_memory(self, data):
        self.heap_memory_view.load_memory(data)
        
    def set_pc(self, pc, last_executed_instruction_address):
        self.code_memory_view.set_current_pc(pc, last_executed_instruction_address)
        
    def update_data_memory(self, modified_data_cells):
        self.data_memory_view.update_memory(modified_data_cells)
        
    def update_heap_memory(self, modified_heap_cells):
        self.heap_memory_view.update_memory(modified_heap_cells)
        
    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
        self.after(20, lambda: 
            self._change_paned_window_appearance(new_appearance_mode)
        ) 
      
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
    
    def _change_paned_window_appearance(self, new_appearance_mode):
        bg_color = self.get_single_color(self.cget("fg_color"))
        self.paned_memory.configure(bg=bg_color, proxybackground=bg_color, background=bg_color)
        self.code_memory_view.change_appearance_mode(new_appearance_mode)
        self.data_memory_view.change_appearance_mode(new_appearance_mode)
        self.heap_memory_view.change_appearance_mode(new_appearance_mode)  
    
    def get_single_color(self, color_tuple):
        """Convert CTk color tuple to single color string based on current appearance mode"""
        if ctk.get_appearance_mode() == "Light":
            return color_tuple[0]  
        else:
            return color_tuple[1] 
