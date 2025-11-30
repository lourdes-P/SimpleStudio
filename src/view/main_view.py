import customtkinter as ctk
from CTkMessagebox.ctkmessagebox import Image, ImageTk
from view.components.controlpanel import ControlPanel
from view.components.dialogs import CustomDialog
from view.components.info_window import InfoWindow
from view.components.input_dialog import InputDialog
from view.components.labelpanel import LabelPanel
from view.components.memorypanel import MemoryPanel
from view.components.output_panel import OutputPanel
from view.file_system_manager import FileSystemManager
import sys
if sys.platform == "win32":
    from ctypes import windll
from view.simplestudio_view_interface import SimpleStudioViewInterface
from view.utils.icon_manager import IconManager

ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme('dark-blue')  # "blue", "green", "dark-blue"

class SimpleStudioViewInterface(ctk.CTk, SimpleStudioViewInterface):
        
    def __init__(self, presenter):
        super().__init__()
        try:
            if sys.platform == "win32":
                windll.shcore.SetProcessDpiAwareness(True)
        except AttributeError:
            pass # not target Windows OS
        self.title("SimpleStudio")
        self.geometry("1200x800")
        self.minsize(800,600)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._set_window_icon()
        
        self._control_panel = None
        self._memory_panel = None
        self._label_panel = None    
        self._output_panel = None
        
        self._info_window = None
        
        self._presenter = presenter
        self._file_system_manager = FileSystemManager(presenter)
        
        self._create_widgets()
        self._setup_layout()
        self._initialize_file_system_manager()
        self._control_panel.initialize()
        self._memory_panel.initialize(self._presenter.on_breakpoint_change)
        
        self._setup_bindings()
        
    def start(self):
        self.mainloop()
        
    def _set_window_icon(self):
        if sys.platform == "win32":
            icon_path = IconManager.SIMPLESTUDIO_ICON_PATH_WIN32
            self.iconbitmap(icon_path, default=icon_path)
        else:
            image= Image.open(IconManager.SIMPLESTUDIO_ICON_PATH_DARWIN_LINUX)
            self.icon_image = ImageTk.PhotoImage(image)
            self.iconphoto(True, self.icon_image)
        
    def _create_widgets(self):
        self._control_panel = ControlPanel(self, step_callback= self._presenter.on_single_step_execution,
                                          run_callback= self._presenter.on_complete_execution,
                                          n_step_callback= self._presenter.on_n_step_execution,
                                          reset_callback=self._presenter.on_reset,
                                          undo_callback= self._presenter.on_undo,
                                          switch_code_editor_callback=self._presenter.on_switch_code_editor,
                                          change_appearance_mode= self.change_appearance_mode, 
                                          browse_file= self._file_system_manager.on_browse_file,
                                          on_save_callback = self._file_system_manager.on_save_file,
                                          on_save_as_callback = self._file_system_manager.on_save_as_file,
                                          show_info_callback= self.show_info)
        
        self._memory_panel = MemoryPanel(self)
        self._label_panel = LabelPanel(self)
        self._output_panel = OutputPanel(self)

    def _setup_layout(self):
        self.grid_columnconfigure((1,2), weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        
        self._control_panel.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self._memory_panel.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")
        self._label_panel.grid(row=2, column=0, padx=5, pady=(0,10), sticky="sw")
        self._output_panel.grid(row=2, column=1, columnspan=2, padx=(0,5), pady=(0,10), sticky="nsew")
        
    def _setup_bindings(self):
        self.bind_all("<Control-h>", lambda _: self._file_system_manager.on_browse_file())
        self.bind_all("<Control-H>", lambda _: self._file_system_manager.on_browse_file())
        self.bind_all("<Control-s>", lambda _: self._file_system_manager.on_save_file())
        self.bind_all("<Control-S>", lambda _: self._file_system_manager.on_save_file())
        self.bind_all("<Control-Shift-s>", lambda _: self._file_system_manager.on_save_as_file())
        self.bind_all("<Control-Shift-S>", lambda _: self._file_system_manager.on_save_as_file())
        self.bind_all("<Control-e>", lambda _: self._control_panel.switch_code_editor())
        self.bind_all("<Control-E>", lambda _: self._control_panel.switch_code_editor())
        self.bind_all("<F5>", lambda _: self._presenter.on_reset())
        self.bind_all("<F7>", lambda _: self._control_panel.on_undo())
        self.bind_all("<F8>", lambda _: self._control_panel.on_step())
        self.bind_all("<F9>", lambda _: self._control_panel.on_n_step())
        self.bind_all("<F10>", lambda _: self._control_panel.on_run())

    def _initialize_file_system_manager(self):
        view_components = {
            'control_panel': self._control_panel,
            'memory_panel': self._memory_panel
        }
        self._file_system_manager.set_view_componets(view_components)
        
    def set_pc(self, pc, last_executed_instruction_address):
        self._memory_panel.set_pc(pc, last_executed_instruction_address)
    
    def get_breakpoints(self):
        return self._memory_panel.get_breakpoints()
    
    def load_code_onto_c_memory(self, code_data, file_path, load_new_file, clear_breakpoints = True):
        try:
            self._memory_panel.load_code_onto_c_memory(code_data, file_path, load_new_file, clear_breakpoints)
        except Exception:
            self.display_error("Error loading file on code editor")
        
    def load_code_editor(self, load_new_file):
        try:
            self._memory_panel.load_code_editor(self.get_selected_file_path(), load_new_file)
        except Exception:
            self.display_error("Error loading file on code editor")
        
    def load_data_memory(self, data):
        self._memory_panel.load_data_memory(data)
        
    def load_heap_memory(self, data):
        self._memory_panel.load_heap_memory(data)
        
    def load_label_panel(self, label_list):
        self._label_panel.load_data(label_list)
        
    def add_labels(self, added_labels_list):
        self._label_panel.add_label_list(added_labels_list) 
      
    def delete_label(self, label_name):
        self._label_panel.delete_label(label_name)
        
    def update_data_memory(self, modified_data_cells):
        self._memory_panel.update_data_memory(modified_data_cells)
        
    def update_heap_memory(self, modified_heap_cells):
        self._memory_panel.update_heap_memory(modified_heap_cells)
    
    def reset(self, parsed_data_memory, parsed_heap_memory, label_list):
        self._memory_panel.reset(parsed_data_memory, parsed_heap_memory)
        self._label_panel.reset(label_list)
        self._output_panel.reset()
        
    def switch_code_editor(self, line_number= None):
        self._memory_panel.switch_code_editor(line_number)
        
    def print_output(self, output_text):
        self._output_panel.append_text_ln(output_text)
        
    def on_save_code_editor(self):
        self._memory_panel.on_save_code_editor()
        
    def set_selected_file_path(self, file_path):
        self._control_panel.set_file_path_label(file_path)
    
    def get_selected_file_path(self):
        return self._control_panel.get_file_path()
        
    def get_selected_code_address(self):
        return self._memory_panel.get_selected_code_address()
        
    def change_appearance_mode(self, new_appearance_mode):
        if new_appearance_mode != ctk.get_appearance_mode():
            ctk.set_appearance_mode(new_appearance_mode)
        
    def display_error(self, message):
        CustomDialog.display_error(self, message)
        
    def display_user_input(self, on_user_input_callback):
        InputDialog.show_input_dialog(on_user_input_callback)
        
    def disable_execution(self):
        self._control_panel.set_buttons_state(False)
        
    def enable_execution(self):
        self._control_panel.set_buttons_state(True)
        
    def set_cache_entry_disponibility(self, number : int):
        if number >= 0:
            self._control_panel.set_cache_entry_disponibility(number)
            
    def show_info(self):
        if self._info_window is None or not self._info_window.winfo_exists():
            self._info_window = InfoWindow(self)
        else:
            self._info_window.focus()

    def _on_closing(self):
        close_window = self._file_system_manager.on_app_close()
        if close_window:
            self.destroy()