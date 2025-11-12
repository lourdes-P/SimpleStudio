import customtkinter as ctk
import tkinter as tk
from view.components.code_editor import CodeEditor
from view.components.codememory import CodeMemoryView
from view.components.data_heap_memory import DataHeapMemoryView
from view.utils.color_manager import ColorManager

class MemoryPanel(ctk.CTkFrame):
    """Component for displaying memory tables (C, D, or H)"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.paned_memory = None
        
        self.code_memory_view = None
        self.cmem_label = None
        self.code_editor_open = False
        self.data_memory_view = None
        self.heap_memory_view = None
        
        self.code_editor = None
        ctk.AppearanceModeTracker.add(self.change_appearance_mode)
        
    def initialize(self, on_breakpoint_change_callback):
        """Create PanedWindow and memories within."""
        bg_color= ColorManager.get_single_color(self.cget("fg_color"))
        
        self.paned_memory = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.FLAT, bg=bg_color,
                                      borderwidth=0, sashwidth=8, showhandle=False, bd=0)
        self.paned_memory.pack(fill="both", expand=True)
                        
        self.create_c_memory(on_breakpoint_change_callback)
        self.create_d_memory()
        self.create_h_memory()
        
    def create_c_memory(self, on_breakpoint_change_callback):     
        self.cmem_container = ctk.CTkFrame(self.paned_memory, corner_radius=0)
        self.cmem_container.grid_rowconfigure(1, weight=1)
        self.cmem_container.grid_columnconfigure(0, weight=1)
        
        self.code_editor = CodeEditor(self.cmem_container)
        self.code_editor.grid(row=0, rowspan=2, column=0, sticky="nsew")
        self.code_editor.grid_remove()
        
        self.cmem_label = ctk.CTkLabel(self.cmem_container, text=" C", font=ctk.CTkFont(weight="bold"), anchor='w')
        self.cmem_label.grid(row=0, column=0, sticky="nsew")
        self.code_memory_view = CodeMemoryView(self.cmem_container)
        self.code_memory_view.grid(row=1, column=0, sticky="nsew")
        
        self.code_memory_view.set_breakpoint_change_callback(on_breakpoint_change_callback)
        self.code_memory_view.change_appearance_mode("System")
        
        self.paned_memory.add(self.cmem_container)
     
    def create_d_memory(self):
        self.dmem_container = ctk.CTkFrame(self.paned_memory, corner_radius=0)
        self.dmem_container.grid_rowconfigure(1, weight=1)
        self.dmem_container.grid_columnconfigure(0, weight=1)
        
        dmem_label = ctk.CTkLabel(self.dmem_container, text=" D", font=ctk.CTkFont(weight="bold"), anchor='w')
        dmem_label.grid(row=0, column=0, sticky="nsew")
        self.data_memory_view = DataHeapMemoryView(self.dmem_container)
        self.data_memory_view.grid(row=1, column=0, sticky="nsew")
        self.data_memory_view.change_appearance_mode("System")

        self.paned_memory.add(self.dmem_container)
    
    def create_h_memory(self):
        self.hmem_container = ctk.CTkFrame(self.paned_memory, corner_radius=0)
        self.hmem_container.grid_rowconfigure(1, weight=1)
        self.hmem_container.grid_columnconfigure(0, weight=1)
        
        hmem_label = ctk.CTkLabel(self.hmem_container, text=" H", font=ctk.CTkFont(weight="bold"), anchor='w')
        hmem_label.grid(row=0, column=0, sticky="nsew")
        self.heap_memory_view = DataHeapMemoryView(self.hmem_container)
        self.heap_memory_view.grid(row=1, column=0, sticky="nsew")
        self.heap_memory_view.change_appearance_mode("System")
        
        self.paned_memory.add(self.hmem_container)
        
    def reset(self, parsed_data_memory, parsed_heap_memory):
        self.data_memory_view.reset(parsed_data_memory)
        self.heap_memory_view.reset(parsed_heap_memory)
        
    def load_code_onto_c_memory(self, code_data, file_path, load_new_file, clear_breakpoints = True):
        self.code_memory_view.load_code(code_data, clear_breakpoints)
        self.code_editor.load_file(file_path, load_new_file)
        
    def load_code_editor(self, file_path, load_new_file):
        if file_path:
            self.code_editor.load_file(file_path, load_new_file)
            
    def on_save_code_editor(self):
        self.code_editor.on_save()
        
    def load_data_memory(self, data):
        self.data_memory_view.load_memory(data)
        
    def load_heap_memory(self, data):
        self.heap_memory_view.load_memory(data)
        
    def switch_code_editor(self, line_number = None):
        if self.code_editor_open:
            self._show_code_memory_view()
        else:
            self._show_code_editor(line_number)
        
    def _show_code_editor(self, line_number = None):
        if self.code_editor:
            if self.code_memory_view.grid_info():
                self.code_memory_view.grid_remove()
                self.cmem_label.grid_remove()
            self.code_editor_open = True
            self.code_editor.grid()
            self.code_editor.open_editor(line_number)
        
    def _show_code_memory_view(self):
        self.code_editor.grid_remove()
        self.code_editor_open = False
        self.cmem_label.grid()
        self.code_memory_view.grid()
        
    def set_pc(self, pc, last_executed_instruction_address):
        self.code_memory_view.set_current_pc(pc, last_executed_instruction_address)
        
    def update_data_memory(self, modified_data_cells):
        self.data_memory_view.update_memory(modified_data_cells)
        
    def update_heap_memory(self, modified_heap_cells):
        self.heap_memory_view.update_memory(modified_heap_cells)
        
    def change_appearance_mode(self, new_appearance_mode):
        self.after(20, lambda: 
            self._change_paned_window_appearance(new_appearance_mode)
        ) 
    
    def get_code_editor_content(self):
        return self.code_editor.get_content()
    
    def code_editor_content_modified(self):
        return self.code_editor.content_modified()
              
    def get_selected_code_address(self):
        return self.code_memory_view.get_selected_address()
      
    def get_code_memory_view(self):
        return self.code_memory_view        
            
    def get_breakpoints(self):
        return self.code_memory_view.get_breakpoints()
    
    def get_code_memory_view(self):
        return self.code_memory_view
    
    def _change_paned_window_appearance(self, new_appearance_mode):
        self.code_editor.update_theme(new_appearance_mode)
        self.code_memory_view.change_appearance_mode(new_appearance_mode)
        self.data_memory_view.change_appearance_mode(new_appearance_mode)
        self.heap_memory_view.change_appearance_mode(new_appearance_mode)  
        bg_color = ColorManager.get_single_color(self.cget("fg_color"))
        self.paned_memory.configure(bg=bg_color,
                                    bd=0,
                                    background=bg_color,
                                    proxybackground=bg_color,
                                    sashrelief=tk.FLAT,
                                    proxyrelief=tk.FLAT)
        