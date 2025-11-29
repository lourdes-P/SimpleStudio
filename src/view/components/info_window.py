import customtkinter as ctk
import re
from view.utils.icon_manager import IconManager

class InfoWindow(ctk.CTkToplevel):
    def __init__(self, master=None, font_family = 'Consolas', font_size = 15, **kwargs):
        super().__init__(master, takefocus= True, **kwargs)
        
        self.title("Info")
        self.geometry("600x600")
        self.minsize(400,400)
        
        self._font_family = font_family
        self._font_size = font_size
        self._font = ctk.CTkFont(family=self._font_family, size=self._font_size)
        
        self._create_widgets()
        self._setup_layout()
        self.after(100, lambda: self.focus())
        self._set_window_icon()
        
    def _set_window_icon(self):
        icon = IconManager.SIMPLESTUDIO_ICON_PATH
        self.wm_iconbitmap()   
        self.after(201, lambda: self.iconbitmap(icon))
        
    def _create_widgets(self):
        self._tabview = ctk.CTkTabview(self)
        
        self._tab_1_grammar = self._tabview.add("Grammar")
        self._tab_2_functionalities = self._tabview.add("Functionalities")
        self._tab_3_shortcuts = self._tabview.add("Shortcuts")
        self._tab_4_about = self._tabview.add("About")
        
        self._create_grammar_text_area()
        self._create_functionalities_text_area()
        self._create_shortcuts_text_area()
        self._create_about_text_area()
        
        self._author_label = ctk.CTkLabel(self, text='Author: Lourdes María Panzone. Assoc. Universidad Nacional del Sur, Argentina.')
    
    def _setup_layout(self):
        self._tabview.pack(side='top', fill="both", expand=True, padx=10, pady=0)
        self._author_label.pack(side='bottom', expand=False, fill='x')
        
        self._tab_1_text_box.pack(fill="both", expand=True, padx=10, pady=10)
        self._tab_2_text_box.pack(fill="both", expand=True, padx=10, pady=10)
        self._tab_3_text_box.pack(fill="both", expand=True, padx=10, pady=10)
        self._tab_4_text_box.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _create_grammar_text_area(self):
        """Create grammar tab text area with formatted content"""
        self._tab_1_text_box = ctk.CTkTextbox(
            self._tab_1_grammar,
            wrap="word",
            font=self._font,
            scrollbar_button_color="#3b3b3b",
            scrollbar_button_hover_color="#4b4b4b",
            tabs=("4c",)
        )
        
        self._set_tags(self._tab_1_text_box)
        
        tab_1_text = """_*Syntaxis*_
Grammar that characterizes syntactically valid programs, written in extended BNF notation:

<Program>       ::=     <Instruction>^+ 
<Instruction>   ::=     Identifier^? <Signatura> annotation^? 
<Signature>     ::=     SetD <Expression>, <Expression> 
                        | SetH <Expression>, <Expression> 
                        | SetActual <Expression> 
                        | SetLibre <Expression> 
                        | SetIn <Expression> 
                        | SetOut <Expression> 
                        | SetPO <Expression> 
                        | SetLabel Identifier, <Expression> 
                        | JumpT <Expression>, <Expression> 
                        | Jump <Expression> 
                        | Halt 
						
<Expression>    ::=     <Expression> <BinaryOp> <Expression> 
                        | <UnaryOp> <Expression> 
                        | <Operand> 
						
<BinaryOp>     ::=      + | - | * | / | % | == | != | < | > | <= | >= | & | |

<UnaryOp>      ::=      + | - | ! 

<Operand>      ::=      D[<Expression>] 
                        | H[<Expression>] 
                        | Actual 
                        | Libre 
                        | Number 
                        | Identifier 
                        | pc 
                        | String
                        | (<Expression>) 
						
Superscript + indicates repetition of a symbol once or more times. Superscript ? indicates symbol is optional.


_*Semantic*_

*SetD Destination, Source*
Instruction used to change the values stored in the D memory. This instruction evaluates the Source expression and stores its result in the D memory, specifically at the address resulting from evaluating the Destination expression.

*SetH Destination, Source*
Instruction used to change the values stored in the H memory. This instruction evaluates the Source expression and stores its result in the H memory, specifically at the address resulting from evaluating the Destination expression.

*SetActual Source*
Instruction used to change the value of Actual. This instruction evaluates the Source expression and assigns its result to the Actual register.

*SetLibre Source*
Instruction used to change the value of Libre. This instruction evaluates the Source expression and assigns its result to the Libre register.

*SetIn Destination*
Instruction used to read values entered by the user, which functions as an integer read. The instruction reads a value from the input and stores it in the D memory, specifically at the address resulting from evaluating the Destination expression.

*SetOut Source*
Instruction used to display values on the screen, which functions as an integer print. The instruction displays the result of evaluating the Source expression on the screen.

*SetPO Source*
Instruction used to change the value of po. This instruction evaluates the Source expression and assigns its result to the po register.

*SetLabel Identifier, Source*
Instruction used to set the value of a Label, which is useful for associating a Label with a memory address (for example, the start of a VT). The instruction creates a label (or changes the value of an existing one) with the name characterized by the Identifier and assigns it the value resulting from evaluating the Source expression.

*JumpT Source, Condition*
Instruction used to perform conditional jumps, modifying the pc. The instruction assigns the value resulting from evaluating the Source expression to the pc register, provided that the value from evaluating the Condition expression is true.

*Jump Source*
Instruction used to perform unconditional jumps, modifying the pc. The instruction assigns the value resulting from evaluating the Source expression to the pc register.

*Halt*
Instruction used to terminate the execution of the currently loaded program.


_*Expression evaluation*_
Binary expressions and unary expressions are evaluated left to right. Operators do have precedence, that analogous to operators in Java or other modern programming languages.
True values include values different from integer 0, and False is represented by integer 0.


_*Disclaimer*_
The information displayed on this window is meant to be a quick summary on the key points of how to use this application. It is *not* a complete guide to nor a complete user manual for the abstract processor SimpleSem or this application, SimpleStudio. Please, refer to the complete documentation to be provided with a proper user manual."""
        
        self._insert_formatted_text(self._tab_1_text_box, tab_1_text)
        self._tab_1_text_box.configure(state="disabled")
    
    def _create_functionalities_text_area(self):
        """Create functionalities tab text area with formatted content"""
        self._tab_2_text_box = ctk.CTkTextbox(
            self._tab_2_functionalities,
            wrap="word",
            font=self._font,
            scrollbar_button_color="#3b3b3b",
            scrollbar_button_hover_color="#4b4b4b",
            tabs=("4c",)
        )
        
        self._set_tags(self._tab_2_text_box)
        
        tab_2_text = """_*Control Panel Functionalities*_

 • *Undo*: Allows the user to undo the execution of the last executed instruction, effectively returning the virtual machine's state to what it was before that instruction was executed. The maximum number of times a user can perform this action consecutively is 10. The number in parentheses indicates how many times the user can currently perform this action at the present moment of the program's execution.
 • *Run*: Allows for the complete execution of the program from the instruction pointed to by the current PC up to a Halt instruction. Execution also terminates in error if a Halt is not found and the PC does not point to a valid address in the code memory.
 • *Step*: Allows the execution of a single instruction at the current PC.
 • *N-step*: Allows the execution of N instructions starting from the current PC. The value of N is taken from the spinner input to the right of the N-step button.
 • *Reset*: Resets the virtual machine and the graphic interface. Additionally, if the file was modified after being loaded, it reloads it.
 • *File Handling Dropdown Menu*: This dropdown menu allows you to choose between loading a file ("Upload Source"), saving the current file to its current path ("Save"), and saving the current file to a new path ("Save As"). It initially reads "Upload Source".
 • *Open Code Editor*/*Open Code Memory*: Allows switching between the code memory view and the code editor.
 • *Appearance Mode Dropdown Menu*: This dropdown menu allows you to change the appearance mode of SimpleStudio. There are three modes: "System", "Dark", and "Light". "System" takes the system's appearance mode ("Light" or "Dark") and applies it to SimpleStudio. "Light" is the light theme, and "Dark" is the dark theme. Initially, it reads "System".
 • *Information Icon* (_*i*_): Opens a window containing information about SimpleStudio and the SimpleSem abstract processor. The information is written in plain text, and its purpose is to provide a quick menu for the most relevant information about the abstract processor and the application.


_*Code Memory (C) Functionalities*_

 • *Annotation tooltips*: for the rows whose cell contains an instruction that has an annotation, the cell's font will be set to bold. If the user hovers the cursor over the Instruction column of a row that has an annotation, the annotation will appear as a tooltip to the right of the code memory.
 • *Breakpoint panel*: located to the left of the table representing the C memory, this panel allows placing a breakpoint on the instruction to its right. A breakpoint is represented by a bullet (or filled circle). When the cursor hovers over the circle representing the breakpoint, it changes to a color different from the background, making it visible. When this circle is clicked, it turns into a vivid red color that doesn't fade, indicating that a breakpoint has been set on the corresponding instruction.
When executing instructions, if the mode is full execution (Run) or N-step execution (N-step), the execution will stop before executing the instruction on which a breakpoint is set.
 • *Row selection*: one row at a time can be selected in the C memory. This selection is used to open the code editor at the end of the line corresponding to the instruction if the "Open Code Editor" button is pressed. When a row is selected, it will be painted a light grayish-blue.


_*Disclaimer*_
The information displayed on this window is meant to be a quick summary on the key points of how to use this application. It is *not* a complete guide to nor a complete user manual for the abstract processor SimpleSem or this application, SimpleStudio. Please, refer to the complete documentation to be provided with a proper user manual."""
        
        self._insert_formatted_text(self._tab_2_text_box, tab_2_text)
        self._tab_2_text_box.configure(state="disabled")
    
    def _create_shortcuts_text_area(self):
        """Create shortcuts tab text area with formatted content"""
        self._tab_3_text_box = ctk.CTkTextbox(
            self._tab_3_shortcuts,
            wrap="word",
            font=self._font,
            scrollbar_button_color="#3b3b3b",
            scrollbar_button_hover_color="#4b4b4b",
            tabs=("4c",)
        )
        
        self._set_tags(self._tab_3_text_box)
        
        tab_3_text = """_*Control Panel Shortcuts*_
 • *Reset*: F5
 • *Undo*: F7
 • *Step*: F8
 • *N-step*: F9
 • *Run*: F10
 • *Upload Source*: Ctrl+h
 • *Save*: Ctrl+s
 • *Save As*: Ctrl+Shift+s
 • *Open Code Editor*/*Open Code Memory*: Ctrl+e


_*Code Editor Shortcuts*_
 • *Ctrl+Backspace*: erases a string of characters so that:
	· if the string starts from a blank, erases backward from the cursor up until the first character different from a blank (exclusive).
	· if the string starts from an alphanumeric character, erases backward from the cursor up until the first blank or the first special character found (exclusive).
	· if the string starts from a special character, erases backward from the cursor up until the first blank or alphanumeric character (exclusive).
It is a try at the common Ctrl+Backspace that can be found in modern text editors.
 • *Ctrl+Del*: similar to Ctrl+Backspace, only that it erases forward from the cursor.
 • *Ctrl+c*: similar to the shortcut Ctrl+C found in code editors. If there is no selected text, it will copy the characters forward from the cursor to the end of the line. 
 • *Ctrl+x*: similar to Ctrl+C, additionally cutting the text from the content.


_*Disclaimer*_
The information displayed on this window is meant to be a quick summary on the key points of how to use this application. It is *not* a complete guide to nor a complete user manual for the abstract processor SimpleSem or this application, SimpleStudio. Please, refer to the complete documentation to be provided with a proper user manual."""
        
        self._insert_formatted_text(self._tab_3_text_box, tab_3_text)
        self._tab_3_text_box.configure(state="disabled")
    
    def _create_about_text_area(self):
        """Create shortcuts tab text area with formatted content"""
        self._tab_4_text_box = ctk.CTkTextbox(
            self._tab_4_about,
            wrap="word",
            font=self._font,
            scrollbar_button_color="#3b3b3b",
            scrollbar_button_hover_color="#4b4b4b",
            tabs=("4c",)
        )
        
        self._set_tags(self._tab_4_text_box)
        
        tab_4_text = """This project was developed by
        _*Lourdes María Panzone*_        
with the guidance of
        _*Dr. María Laura Cobo*_
        _*Dr. Federico Martín Schmidt*_
as the final project of my Bachelor's degree in Computer Science.

Special thanks to my friend María Paz Berterreix who fixed me the logo."""
        
        self._insert_formatted_text(self._tab_4_text_box, tab_4_text)
        self._tab_4_text_box.configure(state="disabled")
    
    def _set_tags(self, text_box : ctk.CTkTextbox):
        text_box._textbox.tag_configure(tagName="bold", font=ctk.CTkFont(family=self._font_family, size= self._font_size, weight="bold"))
        text_box._textbox.tag_configure(tagName="italic", font=ctk.CTkFont(family=self._font_family, size= self._font_size, slant="italic"))
        text_box._textbox.tag_configure(tagName="bold_italic", font=ctk.CTkFont(family=self._font_family, size= self._font_size, weight="bold", slant= "italic"))
        text_box._textbox.tag_configure(tagName="superscript", font=ctk.CTkFont(family=self._font_family, size= self._font_size - 4), offset=4)
    
    def _insert_formatted_text(self, text_widget, text):
        """Insert text with formatting using CTkTextbox tags"""
        # Pattern to match _*text*_, *text*, _text_
        pattern = r'(_\*(.*?)\*_)|(\*(.*?)\*)|(_(.*?)_)|(\^(\S+))'
        
        position = 0
        for match in re.finditer(pattern, text):
            # Text before the match
            before_text = text[position:match.start()]
            if before_text:
                text_widget.insert("end", before_text)
            
            # Determine which pattern matched and apply appropriate tag
            if match.group(1):  # _*text*_ pattern
                content = match.group(2)
                text_widget.insert("end", content, "bold_italic")
            elif match.group(3):  # *text* pattern  
                content = match.group(4)
                text_widget.insert("end", content, "bold")
            elif match.group(5):  # _text_ pattern
                content = match.group(6)
                text_widget.insert("end", content, "italic")
            elif match.group(7):  # ^text pattern (superscript)
                content = match.group(8)
                text_widget.insert("end", content, "superscript")
            
            position = match.end()
        
        # Add any remaining text after the last match
        if position < len(text):
            text_widget.insert("end", text[position:])