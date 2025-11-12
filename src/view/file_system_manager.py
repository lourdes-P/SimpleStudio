from tkinter import filedialog
from view.components.dialogs import CustomDialog

class FileSystemManager:
    
    def __init__(self, presenter):
        self._presenter = presenter
        self._control_panel = None
        self._memory_panel = None
        
    def set_view_componets(self, view_components : dict):
        """Set control panel and memory panel"""
        self._control_panel = view_components['control_panel']
        self._memory_panel = view_components['memory_panel']
    
    def on_browse_file(self):
        if self._memory_panel.code_editor_content_modified():
            if CustomDialog.display_yes_no(self._memory_panel, "Save file changes?", "Save?") == 'Yes':
                self.on_save_file()
                
        file_path = filedialog.askopenfilename(
            title="Select Source File",
            filetypes=[("All files", "*.*"),("Text files", "*.txt"),("SimpleSem files", "*.SimpleSem")]
        )
        if file_path:
            self._control_panel.set_file_path_label(file_path)            
            self._presenter.on_file_selected()
    
    def on_save_file(self):
        file_path = self._control_panel.get_file_path()
        if not file_path or file_path == 'No file selected':
            self.on_save_as_file()
        else:
            content = self._memory_panel.get_code_editor_content()
            if not content:
                if CustomDialog.display_yes_no(self._memory_panel, "The content is empty. Do you want to save an empty file?") != 'Yes':
                    return
            self._presenter.on_save_file(content)
    
    def on_save_as_file(self):
        content = self._memory_panel.get_code_editor_content()
        if not content:
            if CustomDialog.display_yes_no(self._memory_panel, "The content is empty. Do you want to save an empty file?") != 'Yes':
                return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("SimpleStudio files", "*.SimpleStudio"), ("All files", "*.*")]
        )
        if file_path:
            self._presenter.on_save_file(content, file_path=file_path)
        
    def on_app_close(self):
        close_window = True
        if self._memory_panel.code_editor_content_modified():
            reply = CustomDialog.display_yes_no(self._memory_panel, "Save file changes?", "Save?")
            if reply == 'Yes':
                self._file_system_manager.on_save_file()
            elif reply == 'No':
                pass
            else:
                close_window = False
        return close_window