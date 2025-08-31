import customtkinter as ctk

class ControlPanel(ctk.CTkFrame):
    """Component for execution controls"""
    def __init__(self, master, step_callback=None, run_callback=None, 
                 pause_callback=None, reset_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.step_callback = step_callback
        self.run_callback = run_callback
        self.pause_callback = pause_callback
        self.reset_callback = reset_callback
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_label = ctk.CTkLabel(self, text="Control Panel", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(10, 15))
        
        # PC display
        pc_frame = ctk.CTkFrame(self)
        pc_frame.pack(fill='x', padx=10, pady=5)
        
        ctk.CTkLabel(pc_frame, text="PC:").pack(side='left', padx=(10, 5))
        self.pc_value = ctk.CTkLabel(pc_frame, text="0", font=ctk.CTkFont(weight="bold"))
        self.pc_value.pack(side='left')
        
        # Control buttons
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(fill='x', padx=10, pady=15)
        
        self.step_btn = ctk.CTkButton(buttons_frame, text="Step", width=80, command=self.on_step)
        self.step_btn.pack(side='left', padx=5)
        
        self.run_btn = ctk.CTkButton(buttons_frame, text="Run", width=80, command=self.on_run)
        self.run_btn.pack(side='left', padx=5)
        
        self.pause_btn = ctk.CTkButton(buttons_frame, text="Pause", width=80, command=self.on_pause)
        self.pause_btn.pack(side='left', padx=5)
        
        self.reset_btn = ctk.CTkButton(buttons_frame, text="Reset", width=80, command=self.on_reset)
        self.reset_btn.pack(side='left', padx=5)
        
        # Speed control
        speed_frame = ctk.CTkFrame(self)
        speed_frame.pack(fill='x', padx=10, pady=5)
        
        ctk.CTkLabel(speed_frame, text="Speed:").pack(side='left', padx=(10, 5))
        self.speed_slider = ctk.CTkSlider(speed_frame, from_=1, to=10, number_of_steps=9)
        self.speed_slider.pack(side='left', fill='x', expand=True, padx=5)
        self.speed_slider.set(5)  # Default to middle value
        
        # Speed value display
        self.speed_value = ctk.CTkLabel(speed_frame, text="5")
        self.speed_value.pack(side='left', padx=5)
        
        # Bind slider change event
        self.speed_slider.configure(command=self.on_speed_change)
    
    def on_step(self):
        if self.step_callback:
            self.step_callback()
            
    def on_run(self):
        if self.run_callback:
            self.run_callback()
            
    def on_pause(self):
        if self.pause_callback:
            self.pause_callback()
            
    def on_reset(self):
        if self.reset_callback:
            self.reset_callback()
            
    def on_speed_change(self, value):
        self.speed_value.configure(text=str(int(float(value))))
    
    def update_pc(self, value):
        """Update the PC display"""
        self.pc_value.configure(text=str(value))
        
    def set_buttons_state(self, running=False):
        """Enable/disable buttons based on execution state"""
        if running:
            self.step_btn.configure(state="disabled")
            self.run_btn.configure(state="disabled")
            self.pause_btn.configure(state="normal")
        else:
            self.step_btn.configure(state="normal")
            self.run_btn.configure(state="normal")
            self.pause_btn.configure(state="disabled")