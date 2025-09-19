import customtkinter as ctk

class ControlPanel(ctk.CTkFrame):
    """Component for execution controls"""
    def __init__(self, master, step_callback=None, run_callback=None,
                 reset_callback=None, change_appearance_mode = None,
                 browse_file = None, **kwargs):
        super().__init__(master, height=140, corner_radius=0, **kwargs)
        
        self.master = master    # main_view 
        self.step_callback = step_callback
        self.run_callback = run_callback
        self.reset_callback = reset_callback
        self.change_appearance_mode_callback = change_appearance_mode
        self.browse_files_callback = browse_file
        
        
    def initialize(self):
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        
        # Control buttons - arranged horizontally
        self.run_button = ctk.CTkButton(
            self, 
            text="Run",
            command=self.run_callback
        )
        self.run_button.grid(row=0, column=1, padx=20, pady=(20,5))
        
        self.step_button = ctk.CTkButton(
            self, 
            text="Step",
            command=self.step_callback
        )
        self.step_button.grid(row=0, column=2, padx=20, pady=(20,5))
        
        self.reset_button = ctk.CTkButton(
            self, 
            text="Reset",
            command=self.reset_callback
        )
        self.reset_button.grid(row=0, column=3, padx=20, pady=(20,5))
        
        self.upload_button = ctk.CTkButton(
            self,
            text="Upload Source",
            command=self.browse_files_callback
        )
        self.upload_button.grid(row=0, column=4, padx=(20,0), pady=(20,5))  
        
        # Appearance mode option menu
        self.appearance_mode_label = ctk.CTkLabel(
            self, 
            text="Appearance:",
            anchor="w"
        )
        self.appearance_mode_label.grid(row=0, column=6, padx=(20, 2), pady=(20,5))
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self, 
            values=["System", "Dark", "Light"],
            command=self.change_appearance_mode_callback,
            width=100
        )
        self.appearance_mode_optionemenu.grid(row=0, column=7, padx=(0, 20), pady=(20,5))
        
        self.file_path_label = ctk.CTkLabel(
            self, 
            text="No file selected",
            compound="left"
        )
        self.file_path_label.grid(row=1, column=0, columnspan=8, padx=20, pady=(0,1), sticky="w")
    
    def on_step(self):
        if self.step_callback:
            self.step_callback()
            
    def on_run(self):
        if self.run_callback:
            self.run_callback()
            
    def on_reset(self):
        if self.reset_callback:
            self.reset_callback()

    def change_apparance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
    
    def set_change_appearance_mode_callback(self, change_appearance_mode):
        self.change_appearance_mode_callback = change_appearance_mode
        
    def set_file_path_label(self, file_path):
        self.file_path_label.configure(text=file_path)
        
    def get_file_path(self):
        return self.file_path_label.cget("text") if self.file_path_label else None
        
    def set_buttons_state(self, running=False):
        """Enable/disable buttons based on execution state"""
        if running:
            self.step_btn.configure(state="disabled")
            self.run_btn.configure(state="disabled")
            self.reset_btn.configure(state="normal")
        else:
            self.step_btn.configure(state="normal")
            self.run_btn.configure(state="normal")
            self.reset_btn.configure(state="disabled")