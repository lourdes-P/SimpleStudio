import customtkinter as ctk
from typing import Callable, Union, Optional
from CTkMessagebox import CTkMessagebox
# TODO add in documentation pip install CTkMessageBox

class InputDialog(ctk.CTkInputDialog):
    def __init__(
        self,
        callback: Callable[[Union[str, int]], None],
        title: str = "Input",
        text: str = "Enter value:",
        input_type: str = "auto",
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
        self.input_type = input_type
        self.input_value = None
        self.top_level = None
        
    def _ok_event(self, event=None):
        """Override the ok event to handle input validation and callback"""
        input_value = self.get_input()
        
        if not input_value:
            # Show error for empty input
            self._show_error("Input cannot be empty")
            return
        
        try:
            # Process input based on type
            processed_value = self._process_input(input_value)
            
            # Call the callback with the processed value
            self.callback(processed_value)
            
            # Close the dialog
            self.grab_release()
            self.destroy()
            
        except ValueError as e:
            self._show_error(str(e))
    
    def _process_input(self, input_value: str) -> Union[str, int]:
        """Process and validate input based on the specified type"""
        if self.input_type == "integer":
            try:
                return int(input_value)
            except ValueError:
                raise ValueError("Please enter a valid integer")
        elif self.input_type == "string":
            return input_value        
        else: 
            self._show_error("Please enter a valid input.")
    
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
        input_type: str = "auto",
    ) -> None:
        """
        Static method to show the input dialog conveniently.
        
        Example usage:
            InputDialog.show_input_dialog(
                callback=self.handle_input,
                title="Enter value",
                text="Please input a value:",
                input_type="integer"
            )
        """
        dialog = InputDialog(callback, title, text, input_type)
        dialog.wait_window()