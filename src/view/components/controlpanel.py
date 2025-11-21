from pathlib import Path
from CTkMessagebox.ctkmessagebox import Image
import customtkinter as ctk
import tkinter as tk
from view.components.info_window import InfoWindow
from view.components.numeral_spinner import NumeralSpinbox

current_dir = Path(__file__).parent
root = current_dir.parent.parent.parent

class ControlPanel(ctk.CTkFrame):
    """Component for execution controls"""
    def __init__(self, master, step_callback=None, run_callback=None,
                 reset_callback=None, n_step_callback=None, undo_callback = None, 
                 switch_code_editor_callback = None, change_appearance_mode = None, 
                 browse_file = None, on_save_callback = None, on_save_as_callback = None,
                 show_info_callback = None, **kwargs):
        super().__init__(master, height=140, corner_radius=0, **kwargs)
        
        self._step_callback = step_callback
        self._n_step_callback = n_step_callback
        self._run_callback = run_callback
        self._reset_callback = reset_callback
        self._change_appearance_mode_callback = change_appearance_mode
        self._undo_callback = undo_callback
        self._switch_code_editor_callback = switch_code_editor_callback
        self._browse_files_callback = browse_file
        self._on_save_callback = on_save_callback
        self._on_save_as_callback = on_save_as_callback
        self._n_step = 1
        self._cache_entry_disponibility = 0
        self._button_x_padding = 20
        self._show_info_callback = show_info_callback
        self._info_window = None
        
    def initialize(self):
        """Create widgets, setup their layout, and setup bindings."""
        self._create_widgets()
        self._setup_layout()
        self._setup_bindings()
        
    def _create_widgets(self):
        self.undo_button = ctk.CTkButton(
            self, 
            text=f"Undo ({self._cache_entry_disponibility})",
            command=self._undo_callback,
            width=self._calculate_button_width(f"Undo ({self._cache_entry_disponibility})", padding = 10)
        )
        self.run_button = ctk.CTkButton(
            self, 
            text="Run",
            command=self._run_callback,
            width=self._calculate_button_width("Run")
        )
        self.step_button = ctk.CTkButton(
            self, 
            text="Step",
            command=self._step_callback,
            width=self._calculate_button_width("Step")
        )
        
        self.n_step_button = ctk.CTkButton(
            self, 
            text="N-step",
            command=self.on_n_step,
            width=self._calculate_button_width("N-step")
        )
        
        self.n_step_spinbox = NumeralSpinbox(master=self)
        self._n_step = self.n_step_spinbox.get()
        
        self.reset_button = ctk.CTkButton(
            self, 
            text="Reset",
            command=self._reset_callback,
            width=self._calculate_button_width("Reset")
        )
        
        self.upload_button = ctk.CTkButton(
            self,
            text="Upload Source",
            command=self._browse_files_callback,
            width=self._calculate_button_width("Upload Source")
        )
        
        self.file_managing_menu = ctk.CTkOptionMenu(
            self, 
            values=["Upload Source", "Save", "Save As"],
            command=self._on_file_menu_selected,
            width=self._calculate_button_width("Upload Source"),
            anchor='center'
        )
        
        self.code_editor_button = ctk.CTkButton(
            self, 
            text="Open Code Editor",
            command=self.switch_code_editor,
            width=self._calculate_button_width("Open Code Editor", 5)
        )
        
        light_image_path = root/'resources'/'info_light.png'
        dark_image_path = root/'resources'/'info_dark.png'
        icon = ctk.CTkImage(Image.open(light_image_path), Image.open(dark_image_path), size=(22,22))
        self._about_button = ctk.CTkButton(
            self, 
            text='',
            command=self.show_info,
            width=1,
            height=1,
            image=icon,
            border_spacing=0,
            border_width=0,
            fg_color='transparent',
            hover=False,
        )
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self, 
            values=["System", "Dark", "Light"],
            command=self._change_appearance_mode_callback,
            width=self._calculate_button_width("System")
        )
        
        self.file_path_label = ctk.CTkLabel(
            self, 
            text="No file selected",
            compound="left"
        )
        
        self.set_buttons_state(False) 
        
    def _setup_layout(self):
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 9), weight=0, minsize=5)
        self.grid_columnconfigure((0,8), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.undo_button.grid(row=0, column=1, padx=self._button_x_padding, pady=(20,5), sticky="ew")
        self.run_button.grid(row=0, column=2, padx=self._button_x_padding, pady=(20,5), sticky="ew")
        self.step_button.grid(row=0, column=3, padx=self._button_x_padding, pady=(20,5), sticky="ew")
        self.n_step_button.grid(row=0, column=4, padx=(self._button_x_padding, 0), pady=(20,5), sticky="ew")
        self.n_step_spinbox.grid(row=0, column=5, padx=(0, self._button_x_padding), pady=(20,5))
        self.reset_button.grid(row=0, column=6, padx=self._button_x_padding, pady=(20,5), sticky="ew")
        self.file_managing_menu.grid(row=0, column=7, padx=(self._button_x_padding,0), pady=(20,5))  
        self.code_editor_button.grid(row=1, column=7, padx=(self._button_x_padding,0), pady=(0,10))
        self._about_button.grid(row=0, column=9, padx=self._button_x_padding, pady=(20,5), sticky="ne")
        self.appearance_mode_optionemenu.grid(row=1, column=9, padx=self._button_x_padding, pady=(0,10), sticky="se")
        self.file_path_label.grid(row=1, column=0, columnspan=7, padx=self._button_x_padding, pady=(0,1), sticky="w")

    def _setup_bindings(self):
        self.bind("<Configure>", self._on_window_resize)

    def on_undo(self):
        if self._undo_callback and self._get_button_state(self.undo_button) == ctk.NORMAL:
            self._undo_callback()
            
    def on_run(self):
        if self._run_callback and self._get_button_state(self.run_button) == ctk.NORMAL:
            self._run_callback()
            
    def on_step(self):
        if self._step_callback and self._get_button_state(self.step_button) == ctk.NORMAL:
            self._step_callback()
            
    def on_n_step(self):
        if self._n_step_callback and self._get_button_state(self.n_step_button) == ctk.NORMAL:
            self._n_step = self.n_step_spinbox.get()
            if self._n_step > 0:
                self._n_step_callback(self._n_step)
                
    def _on_file_menu_selected(self, option_selected):
        if option_selected == 'Upload Source':
            self._browse_files_callback()
        elif option_selected == 'Save':
            self._on_save_callback()
        elif option_selected == 'Save As':
            self._on_save_as_callback()
    
    def switch_code_editor(self):
        self._toggle_code_editor_button()
        self._switch_code_editor_callback()
        
    def show_info(self):
        if self._show_info_callback is not None:
            self._show_info_callback()
        
    def _toggle_code_editor_button(self):
        if self.code_editor_button.cget("text") == "Open Code Editor":
            self.code_editor_button.configure(text="Open Code Memory", width=self._calculate_button_width("Open Code Memory", 5))
        else:
            self.code_editor_button.configure(text="Open Code Editor", width=self._calculate_button_width("Open Code Editor", 5))
            
    def set_cache_entry_disponibility(self, number : int):
        self._cache_entry_disponibility = number
        self.undo_button.configure(
            text=f"Undo ({self._cache_entry_disponibility})",
            width=self._calculate_button_width(f"Undo ({self._cache_entry_disponibility})", padding = 10)
            )
        if number > 0:  
            self.undo_button.configure(state='normal')
        else:
            self.undo_button.configure(state='disabled')
    
    def set_change_appearance_mode_callback(self, change_appearance_mode):
        self._change_appearance_mode_callback = change_appearance_mode
        
    def set_file_path_label(self, file_path):
        self.file_path_label.configure(text=file_path)
        
    def get_file_path(self):
        return self.file_path_label.cget("text") if self.file_path_label else None
        
    def set_buttons_state(self, enabled=False):
        """Enable/disable buttons with boolean value (True enabled, False disabled)"""
        if enabled is True:
            if self._cache_entry_disponibility > 0:
                self.undo_button.configure(state="normal")
            self.step_button.configure(state="normal")
            self.n_step_button.configure(state="normal")
            self.run_button.configure(state="normal")
        else:
            self.undo_button.configure(state="disabled")
            self.step_button.configure(state="disabled")
            self.n_step_button.configure(state="disabled")
            self.run_button.configure(state="disabled")
       
    def _get_button_state(self, button_widget):
        return button_widget.cget('state')
            
    def _calculate_button_width(self, text, padding=20):
        """Calculate appropriate width based on text length"""
        base_width = len(text) * 8 + padding
        return max(50, base_width)
    
    def _change_button_x_padding(self):
        width = self.winfo_width()
        former_x_padding = self._button_x_padding
        if width < 600:
            self._button_x_padding = 5
        elif width <= 800:
            self._button_x_padding = 10
        else:
            self._button_x_padding = 20
        return (former_x_padding, self._button_x_padding)

    def _on_window_resize(self, event):
        x_padding_tuple = self._change_button_x_padding()
        if (x_padding_tuple[0] != x_padding_tuple[1]):
            self._setup_layout()