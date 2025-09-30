import customtkinter as ctk

from view.components.dualscrollframe import DualScrollFrame

class OutputPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, height=150, **kwargs)
        
        self._create_widgets()
        self._setup_layout()
        
    def _create_widgets(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=22)
        self.header_frame.grid_columnconfigure(0, minsize=100)
        
        self.output_header = ctk.CTkLabel(self.header_frame, text="Output", width=100, anchor="w")
        
        self.output_frame =  DualScrollFrame(self, height=150)
        self.output_label = ctk.CTkLabel(self.output_frame.get_scrollable_frame(), text='')
        
    def _setup_layout(self):
        self.grid_propagate(False)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(2, 0))
        self.output_header.grid(row=0, column=0, padx=2, pady=2, sticky="w")
        
        self.output_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 5))
        self.output_label.grid()
        
    def set_output_text(self, text):
        self.output_label.configure(text=text)
        
    def append_text_ln(self, text):
        former_text = self.output_label.cget('text')
        self.set_output_text(f"{former_text}{text}\n")
        
    def get_output_text(self):
        return self.output_label.cget('text')
    
    def reset(self):
        self.output_label.configure(text='')