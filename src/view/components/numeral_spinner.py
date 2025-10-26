import customtkinter as ctk
from typing import Union, Callable

# from Tom Schimansky's Spinbox (see the link below):
# https://github.com/TomSchimansky/CustomTkinter/wiki/Create-new-widgets-(Spinbox) 
# Edited lightly so that the buttons are on the right and it
# only accepts integers > 0 and validates each keystroke.

class NumeralSpinbox(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, int] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command
        self.grid_columnconfigure((1, 2), weight=0)
        self.grid_columnconfigure(0, minsize= 50, weight=1)
        vcmd = (self.register(self.validate))
        self.entry = ctk.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0, validate='all', validatecommand=(vcmd, '%P'))
        self.entry.grid(row=0, column=0, columnspan=1, padx=3, pady=3, sticky="nsew")
        
        self.subtract_button = ctk.CTkButton(self, text='-', width=height-6, 
                                             height=height-6, anchor='center',
                                             command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=1, padx=(3, 0), pady=3)

        self.add_button = ctk.CTkButton(self, text="+", width=height-6, 
                                        height=height-6, anchor='center',
                                        command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        self.entry.insert(0, "1")

    def add_button_callback(self):
        try:
            value = self.get()
            value = value + self.step_size if value > 0 else + self.step_size
            self.entry.delete(0, "end") 
            self.entry.insert(0, value)
        except ValueError:
            return
        if self.command is not None:
            self.command()

    def subtract_button_callback(self):
        try:
            value = self.get() - self.step_size
            value = value if value > 0 else 1
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return
        if self.command is not None:
            self.command()

    def get(self) -> Union[int, None]:
        """If it is an int < 0, it will set the entry to 1 and return 1.
        If it is not an int, it will set the entry to one and return 0 (treat as invalid)."""
        try:
            return int(self.entry.get()) if int(self.entry.get())>0 else self.set(1)
        except ValueError:
            self.set(1)
            return int(0)

    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))
        return int(self.entry.get())
    
    def validate(self, P):
        return str.isdigit(P) or str(P)==""
        