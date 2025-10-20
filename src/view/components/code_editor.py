import tkinter as tk
import customtkinter as ctk
from tkinter import scrolledtext
from tkinter import font

class CodeEditor(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Get current theme colors
        self.appearance_mode = ctk.get_appearance_mode()
        self.font_name = "Consolas"
        self.font_size = 11
        self.last_line_count = 0
        self._setup_colors()
        
        self._create_widgets()
        self._setup_bindings()
    
    def _setup_colors(self):
        """Get colors based on current appearance mode"""
        if self.appearance_mode == "Dark":
            self.bg_color = "#2b2b2b"
            self.fg_color = "#ffffff"
            self.line_bg = "#3c3c3c"
            self.line_fg = "#888888"
            self.highlight_color = "#366693"
        else:  # Light mode
            self.bg_color = "#ffffff"
            self.fg_color = "#000000"
            self.line_bg = "#f0f0f0"
            self.line_fg = "#666666"
            self.highlight_color = "#d6eaff"
    
    def _create_widgets(self):
        # Main container
        self.main_container = tk.Frame(self, bg=self.bg_color)
        self.main_container.pack(fill="both", expand=True)
        self.main_container.grid_columnconfigure((0,2), weight=0)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure((0,2), weight=0)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.line_numbers = tk.Text(
            self.main_container,
            width=4,
            padx=4,
            pady=5,
            bg=self.line_bg,
            fg=self.line_fg,
            relief="flat",
            border=0,
            state="disabled",
            wrap="none",
            font=(self.font_name, self.font_size)
        )
        self.line_numbers.grid(column=0, row=1, rowspan=2, sticky="ns")
        
        self.text_area = tk.Text(
            self.main_container,
            pady=5,
            padx=5,
            bg=self.bg_color,
            fg=self.fg_color,
            relief="flat",
            border=0,
            undo=True,
            wrap="none",
            font=(self.font_name, self.font_size),
            insertbackground=self.fg_color,  # Cursor color
            selectbackground=self.highlight_color  # Selection color
        )
        self.text_area.grid(row=1, column=1, sticky="nsew")
        
        self.v_scrollbar = ctk.CTkScrollbar(
            self.main_container, 
            orientation="vertical",
            command=self._on_vertical_scroll
        )
        self.v_scrollbar.grid(row=1, column=2, sticky="ns")
        
        self.h_scrollbar = ctk.CTkScrollbar(
            self.main_container,
            orientation="horizontal",
            command=self._on_horizontal_scroll
        )
        self.h_scrollbar.grid(row=2,column=1, sticky= "nsew")
        
        self.text_area.configure(
            yscrollcommand=self._on_text_vertical_scroll,
            xscrollcommand=self._on_text_horizontal_scroll
        )
        
        self.line_numbers.configure(yscrollcommand=self._on_line_scroll)
        
        self._update_line_numbers()
    
    def _setup_bindings(self):
        self.text_area.bind("<KeyRelease>", self.on_text_change)
        self.text_area.bind("<MouseWheel>", self._on_mousewheel)
        self.text_area.bind("<Button-4>", self._on_mousewheel)
        self.text_area.bind("<Button-5>", self._on_mousewheel)
        self.text_area.bind("<Shift-MouseWheel>", self._on_shift_mousewheel)
        self.text_area.bind("<Configure>", self._on_configure)
        # Enhanced key bindings
        self.text_area.bind("<Control-Key-BackSpace>", self._ctrl_backspace)
        self.text_area.bind("<Control-Key-Delete>", self._ctrl_delete)
        self.text_area.bind("<Control-Key-c>", self._ctrl_c)
        self.text_area.bind("<Control-Key-x>", self._ctrl_x)
        self.text_area.bind("<Control-Key-C>", self._ctrl_c)
        self.text_area.bind("<Control-Key-X>", self._ctrl_x)
    
    def _ctrl_backspace(self, event):
        """Delete from cursor to previous word boundary (space, special char, or start of word)"""
        # Get current cursor position
        cursor_pos = self.text_area.index(tk.INSERT)
        
        # Get the text from start of line to cursor
        line_start = self.text_area.index(f"{cursor_pos} linestart")
        text_before_cursor = self.text_area.get(line_start, cursor_pos)
        
        if not text_before_cursor:  # If we're at the start of line, nothing to delete
            return "break"
        
        # Find the previous boundary (space, special character, or different character type)
        delete_length = 0
        # Check characters backwards from cursor
        for i in range(len(text_before_cursor) - 1, -1, -1):
            char = text_before_cursor[i]
            
            if i == len(text_before_cursor) - 1:
                # This is the character immediately before cursor
                if char.isspace():
                    # Delete all consecutive whitespace backwards
                    delete_length += 1
                    continue
                elif char.isalnum():
                    # Delete until non-alphanumeric or space
                    delete_length += 1
                    continue
                else:
                    # Delete until different type of character or space
                    delete_length += 1
                    continue
            
            # Check if we should continue deleting
            prev_char = text_before_cursor[i + 1]  # The character we were previously checking
            current_char = text_before_cursor[i]   # The character we're currently checking
            
            if prev_char.isspace():
                # If we were deleting whitespace, stop at non-whitespace
                if not current_char.isspace():
                    break
                delete_length += 1
            elif prev_char.isalnum():
                # If we were deleting alphanumeric, stop at non-alphanumeric
                if not current_char.isalnum():
                    break
                delete_length += 1
            else:
                # If we were deleting special chars, stop at different type or alphanumeric
                if current_char.isspace() or current_char.isalnum():
                    break
                delete_length += 1
        
        # Delete the calculated range
        if delete_length > 0:
            delete_start = self.text_area.index(f"{cursor_pos}-{delete_length}c")
            self.text_area.delete(delete_start, cursor_pos)
        
        return "break"  # Prevent default behavior
    
    def _ctrl_delete(self, event):
        """Delete from cursor to next word boundary (space, special char, or end of word)"""
        # Get current cursor position
        cursor_pos = self.text_area.index(tk.INSERT)
        
        # Get the text from cursor to end of line
        line_end = self.text_area.index(f"{cursor_pos} lineend")
        text_after_cursor = self.text_area.get(cursor_pos, line_end)
        
        if not text_after_cursor:  # If we're at the end of line, nothing to delete
            return "break"
        
        # Find the next boundary (space, special character, or different character type)
        delete_length = 0
        first_char = text_after_cursor[0]
        
        # Check if we're starting with whitespace
        if first_char.isspace():
            # Delete all consecutive whitespace
            for char in text_after_cursor:
                if char.isspace():
                    delete_length += 1
                else:
                    break
        else:
            # Check if first character is alphanumeric
            if first_char.isalnum():
                # Delete until non-alphanumeric or space
                for char in text_after_cursor:
                    if char.isalnum():
                        delete_length += 1
                    else:
                        break
            else:
                # Delete until different type of character or space
                for char in text_after_cursor:
                    if not char.isspace() and not char.isalnum():
                        delete_length += 1
                    else:
                        break
        
        # Delete the calculated range
        if delete_length > 0:
            delete_end = self.text_area.index(f"{cursor_pos}+{delete_length}c")
            self.text_area.delete(cursor_pos, delete_end)
        
        return "break"  # Prevent default behavior
    
    def _ctrl_c(self, event):
        """Enhanced Ctrl+C: if no selection, copy from cursor to end of line"""
        try:
            # Check if there's a selection
            if self.text_area.tag_ranges(tk.SEL):
                # Use default copy behavior if there's a selection
                self.text_area.event_generate("<<Copy>>")
            else:
                # No selection - copy from cursor to end of line
                cursor_pos = self.text_area.index(tk.INSERT)
                line_end = self.text_area.index(f"{cursor_pos} lineend")
                text_to_copy = self.text_area.get(cursor_pos, line_end)
                
                if text_to_copy:
                    self.clipboard_clear()
                    self.clipboard_append(text_to_copy)
            
            return "break"
        except tk.TclError:
            # Fallback to default behavior if something goes wrong
            self.text_area.event_generate("<<Copy>>")
            return "break"
    
    def _ctrl_x(self, event):
        """Enhanced Ctrl+X: if no selection, cut from cursor to end of line"""
        try:
            # Check if there's a selection
            if self.text_area.tag_ranges(tk.SEL):
                # Use default cut behavior if there's a selection
                self.text_area.event_generate("<<Cut>>")
            else:
                # No selection - cut from cursor to end of line
                cursor_pos = self.text_area.index(tk.INSERT)
                line_end = self.text_area.index(f"{cursor_pos} lineend")
                text_to_cut = self.text_area.get(cursor_pos, line_end)
                
                if text_to_cut:
                    self.clipboard_clear()
                    self.clipboard_append(text_to_cut)
                    self.text_area.delete(cursor_pos, line_end)
            
            return "break"
        except tk.TclError:
            # Fallback to default behavior if something goes wrong
            self.text_area.event_generate("<<Cut>>")
            return "break"
    
    def _on_vertical_scroll(self, *args):
        """Handle vertical scrolling for both text and line numbers"""
        self.text_area.yview(*args)
        self.line_numbers.yview(*args)
    
    def _on_horizontal_scroll(self, *args):
        """Handle horizontal scrolling for text area"""
        self.text_area.xview(*args)
    
    def _on_text_vertical_scroll(self, *args):
        """Sync vertical scrollbar with text scrolling"""
        self.v_scrollbar.set(*args)
        self.line_numbers.yview_moveto(args[0])
    
    def _on_text_horizontal_scroll(self, *args):
        """Sync horizontal scrollbar with text scrolling"""
        self.h_scrollbar.set(*args)
    
    def _on_line_scroll(self, *args):
        """Sync line numbers with vertical scrolling"""
        self.v_scrollbar.set(*args)
        self.text_area.yview_moveto(args[0])
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        if event.delta:
            self.text_area.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            self.text_area.yview_scroll(int(-1 * event.num), "units")
        return "break"
    
    def _on_shift_mousewheel(self, event):
        """Handle Shift+MouseWheel for horizontal scrolling (optional)"""
        if event.delta:
            self.text_area.xview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            self.text_area.xview_scroll(int(-1 * event.num), "units")
        return "break"
    
    def _on_configure(self, event=None):
        """Update scrollbar visibility when widget is resized"""
        self._update_horizontal_scrollbar_visibility()
    
    def _update_horizontal_scrollbar_visibility(self):
        """Show/hide horizontal scrollbar based on content width"""
        longest_line_width = self._get_longest_line_width()
        
        text_width = self.text_area.winfo_width()
        
        if longest_line_width > text_width:
            self.h_scrollbar.grid(row=2,column=1, sticky= "nsew")
        else:
            self.h_scrollbar.grid_remove()
    
    def _get_longest_line_width(self):
        """Calculate the width of the longest line in pixels"""
        try:
            content = self.text_area.get("1.0", "end-1c")
            lines = content.split('\n')
            
            if not lines:
                return 0
            
            text_font = self.text_area.cget("font")
            font_metrics = tk.font.Font(self.text_area, font=text_font)
            
            max_width = 0
            padding = 20
            for line in lines:
                line_width = font_metrics.measure(line)
                max_width = max(max_width, line_width)
            
            return max_width + padding
            
        except Exception as e:
            print(f"Error calculating line width: {e}")
            return 0
    """
    def on_text_change(self, event=None):
        self._update_line_numbers()
        self.after(10, self._update_horizontal_scrollbar_visibility)"""
    
    def on_text_change(self, event=None):
        """Handle text changes, but don't interfere with special keys"""
        # Ignore special keys that don't actually change text
        if event and event.keysym in ['Left', 'Right', 'Up', 'Down', 'Prior', 'Next', 
                                    'Home', 'End', 'Delete', 'BackSpace']:
            return
        
        # Also ignore control key combinations that don't change text
        if event and event.state & 0x0004:  # Control key pressed
            if event.keysym in ['c', 'C', 'x', 'X', 'v', 'V', 'a', 'A']:
                return
        
        self._update_line_numbers()
        self.after(10, self._update_horizontal_scrollbar_visibility)
    
    def _update_line_numbers(self):
        current_line_count = int(self.text_area.index('end-1c').split('.')[0])
        
        if hasattr(self, 'last_line_count'):
            last_line_count = self.last_line_count
        else:
            last_line_count = 0
            self.last_line_count = 0
        
        if current_line_count == last_line_count:
            return
            
        self.line_numbers.config(state="normal")
        
        if current_line_count > last_line_count:
            new_lines = "\n".join(str(i) for i in range(last_line_count + 1, current_line_count + 1))
            if last_line_count == 0:
                # First time or complete refresh needed
                self.line_numbers.delete("1.0", "end")
                self.line_numbers.insert("1.0", new_lines)
            else:
                self.line_numbers.insert("end", "\n" + new_lines)
        
        elif current_line_count < last_line_count:
            self.line_numbers.delete(f"{current_line_count + 1}.0", "end")
        
        self.last_line_count = current_line_count
        self.line_numbers.config(state="disabled")
        
    def _move_cursor_to_line_end(self, line_number):
        """Move cursor to the end of specified line number"""
        index = f"{line_number}.end"
        self.text_area.mark_set("insert", index)
        self.text_area.see(index)
        self.text_area.focus_set()
    
    def load_file(self, file_path):
        """Load file content into editor"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", content)
            self._update_line_numbers()
        except Exception as e:
            print(f"Error loading file: {e}")
    
    def open_editor(self, line_number = None):
        if line_number:
            self._move_cursor_to_line_end(line_number)
        else: 
            pass # TODO open editor if not line number
        
    def get_content(self):
        return self.text_area.get("1.0", "end-1c")
    
    def update_theme(self, theme):
        """Update colors when appearance mode changes"""
        self.appearance_mode = theme
        self._setup_colors()
        self.text_area.configure(
            bg=self.bg_color,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            selectbackground=self.highlight_color
        )
        self.line_numbers.configure(
            bg=self.line_bg,
            fg=self.line_fg
        )
        self.main_container.configure(bg=self.bg_color)
        
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("VM Code Editor")
        self.geometry("800x600")
        
        # Theme switcher
        self.theme_button = ctk.CTkButton(
            self, 
            text="Toggle Theme", 
            command=self.toggle_theme
        )
        self.theme_button.pack(pady=10)
        
        # Code editor
        self.editor = CodeEditor(self)
        self.editor.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load sample content
        self.editor.text_area.insert("1.0", "# Sample code\nprint('Hello, World!')\nfor i in range(10):\n    print(i)")
        self.editor._update_line_numbers()
    
    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        new_mode = "Light" if current == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        self.editor.update_theme(new_mode)

if __name__ == "__main__":
    app = App()
    app.mainloop()