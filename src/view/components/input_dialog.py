import customtkinter as ctk
from typing import Callable, Union
from CTkMessagebox import CTkMessagebox

class InputDialog(ctk.CTkInputDialog):
    def __init__(
        self,
        callback: Callable[[Union[str, int]], None],
        title: str = "Input",
        text: str = "Enter value:",
        **kwargs
    ):
        """
        Custom input dialog for virtual machine input.
        
        Args:
            callback: Function to call when user inputs data
            title: Dialog window title
            text: Prompt text for the user
            input_type: Type of input expected - "auto", "string", or "integer"
        """
        super().__init__(title=title, text=text, **kwargs)
        self.callback = callback
        self.input_value = None
        self.top_level = None
        
    def _ok_event(self, event=None):
        """Override the ok event to handle input validation and callback"""
        self._user_input = self._entry.get()

        if not self._user_input:
            self._show_error("Input cannot be empty")
            return
        
        try:            
            self.callback(self._user_input)
             
        except ValueError as e:
            self._show_error(str(e))
        finally:
            self.grab_release()
            self.destroy()
    
    def _cancel_event(self):
        """Override cancel event so that it shows an error"""
        self._show_error("Input cannot be empty")
        
    def _on_closing(self):
        """Override on closing so that it shows an error"""
        self._show_error("Input cannot be empty")
    
    def _show_error(self, message: str):
        """Show error message to user"""
        error_box = CTkMessagebox(
            title="ERROR",
            message=message,
            icon="cancel",
            option_1="OK",
            width= self.winfo_width(),
            height=self.winfo_height(),
            master=self
        )
        
    def destroy(self):
        if self.top_level and self.top_level.winfo_exists():
            self.top_level.destroy()
        super().destroy()
    
    @staticmethod
    def show_input_dialog(
        callback: Callable[[Union[str, int]], None],
        title: str = "Input",
        text: str = "Enter value:",
        **kwargs
    ) -> None:
        """
        Static method to show input dialog.
        
        Example usage:
                callback=self.handle_input,
                title="Enter value",
                text="Please input a value:",
                **kwargs
            )
        """
        dialog = InputDialog(callback, title, text, **kwargs)
        dialog.wait_window()