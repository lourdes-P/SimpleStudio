import customtkinter as ctk
from view.components.numeral_spinner import NumeralSpinbox

class ControlPanel(ctk.CTkFrame):
    """Component for execution controls"""
    def __init__(self, master, step_callback=None, run_callback=None,
                 reset_callback=None, n_step_callback=None, change_appearance_mode = None,
                 browse_file = None, **kwargs):
        super().__init__(master, height=140, corner_radius=0, **kwargs)
        
        self.step_callback = step_callback
        self.n_step_callback = n_step_callback
        self.run_callback = run_callback
        self.reset_callback = reset_callback
        self.change_appearance_mode_callback = change_appearance_mode
        self.browse_files_callback = browse_file
        self.n_step = 1
        
    def initialize(self):
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6, 8), weight=0, minsize=5)
        self.grid_columnconfigure((0,7), weight=1)
        
        self.run_button = ctk.CTkButton(
            self, 
            text="Run",
            command=self.run_callback,
            width=self._calculate_button_width("Run")
        )
        self.run_button.grid(row=0, column=1, padx=20, pady=(20,5), sticky="ew")
        self.step_button = ctk.CTkButton(
            self, 
            text="Step",
            command=self.step_callback,
            width=self._calculate_button_width("Step")
        )
        self.step_button.grid(row=0, column=2, padx=20, pady=(20,5), sticky="ew")
        
        self.n_step_button = ctk.CTkButton(
            self, 
            text="N-step",
            command=self.on_n_step,
            width=self._calculate_button_width("N-step")
        )
        self.n_step_button.grid(row=0, column=3, padx=(20, 0), pady=(20,5), sticky="ew")
        
        self.n_step_spinbox = NumeralSpinbox(master=self)
        self.n_step_spinbox.grid(row=0, column=4, padx=(0, 20), pady=(20,5))
        self.n_step = self.n_step_spinbox.get()
        
        self.reset_button = ctk.CTkButton(
            self, 
            text="Reset",
            command=self.reset_callback,
            width=self._calculate_button_width("Reset")
        )
        self.reset_button.grid(row=0, column=5, padx=20, pady=(20,5), sticky="ew")
        
        self.upload_button = ctk.CTkButton(
            self,
            text="Upload Source",
            command=self.browse_files_callback,
            width=self._calculate_button_width("Upload Source")
        )
        self.upload_button.grid(row=0, column=6, padx=(20,0), pady=(20,5))  
        
        # Appearance mode option menu
        self.appearance_mode_label = ctk.CTkLabel(
            self, 
            text="Appearance:",
            anchor="sw"
        )
        self.appearance_mode_label.grid(row=0, column=8, padx=20, pady=(20,5), sticky="ne")
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self, 
            values=["System", "Dark", "Light"],
            command=self.change_appearance_mode_callback,
            width=self._calculate_button_width("System")
        )
        self.appearance_mode_optionemenu.grid(row=1, column=8, padx=20, pady=(0,10), sticky="se")
        
        self.file_path_label = ctk.CTkLabel(
            self, 
            text="No file selected",
            compound="left"
        )
        self.file_path_label.grid(row=1, column=0, columnspan=8, padx=20, pady=(0,1), sticky="w")
        
        self.set_buttons_state(False)
    
    def on_step(self):
        if self.step_callback:
            self.step_callback()
            
    def on_run(self):
        if self.run_callback:
            self.run_callback()
            
    def on_reset(self):
        if self.reset_callback:
            self.reset_callback()
            
    def on_n_step(self):
        if self.n_step_callback:
            self.n_step = self.n_step_spinbox.get()
            if self.n_step > 0:
                self.n_step_callback(self.n_step)

    def change_apparance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
    
    def set_change_appearance_mode_callback(self, change_appearance_mode):
        self.change_appearance_mode_callback = change_appearance_mode
        
    def set_file_path_label(self, file_path):
        self.file_path_label.configure(text=file_path)
        
    def get_file_path(self):
        return self.file_path_label.cget("text") if self.file_path_label else None
        
    def set_buttons_state(self, enabled=False):
        """Enable/disable buttons with boolean value (True enabled, False disabled)"""
        if enabled is True:
            self.step_button.configure(state="normal")
            self.n_step_button.configure(state="normal")
            self.run_button.configure(state="normal")
        else:
            self.step_button.configure(state="disabled")
            self.n_step_button.configure(state="disabled")
            self.run_button.configure(state="disabled")
            
    def _calculate_button_width(self, text, padding=20):
        """Calculate appropriate width based on text length"""
        base_width = len(text) * 8 + padding
        return max(50, base_width)