import tkinter as tk
import customtkinter as ctk
from view.utils.color_manager import ColorManager
from view.utils.time import debounce

class CodeEditor(ctk.CTkFrame):
    
    END_MINUS_ONE_CHAR = "end-1c"
    START = "1.0"
    
    def __init__(self, parent, font_name = 'Consolas', font_size = 15, **kwargs):
        super().__init__(parent, **kwargs)
        self._appearance_mode = ctk.get_appearance_mode()
        self._font = ctk.CTkFont(font_name, font_size)
        self._last_line_count = 0
        self._initial_content = ''
        self._create_widgets()
        self._setup_bindings()
    
    def load_file(self, file_path, load_new_file = True):
        """Load file content into editor"""
        try:
            cursor_position = self.text_area.index(tk.INSERT)
            with open(file_path, 'r', encoding='utf-8') as file:
                self._initial_content = file.read()
            self._replace_content(self._initial_content)
            
            if load_new_file:
                self.text_area.edit_reset()
                cursor_position = self.START
            
            self._move_cursor_to(cursor_position)
            self._update_line_numbers()
            self._update_scrollbar_visibility()
        except Exception as e:
            print(f"Error loading file: {e}")
    
    def open_editor(self, line_number = None):
        if line_number is not None:
            index = f"{line_number}.end"
            self._move_cursor_to(index)
        
    def get_content(self):
        return self.text_area.get(self.START, self.END_MINUS_ONE_CHAR)
    
    def content_modified(self):
        return self.get_content() != self._initial_content
    
    def on_save(self):
        self._initial_content = self.get_content()
    
    def update_theme(self, theme):
        """Update colors when appearance mode changes"""
        self._appearance_mode = theme
        if theme == 'System':
            self._appearance_mode = ctk.get_appearance_mode()
        else:
            self._appearance_mode = theme
        self.text_area.configure(
            bg=self._get_colors('text_background_color'),
            fg=self._get_colors('text_color'),
            insertbackground=self._get_colors('cursor_color'),
            selectbackground=self._get_colors('highlight_color'),
            selectforeground=self._get_colors('highlight_text_color')
        )
        self.line_numbers.configure(
            bg=self._get_colors('line_number_background_color'),
            fg=self._get_colors('line_number_text_color')
        )
        self._excess_frame.configure(
            bg=self._get_colors('line_number_background_color'),
        )
        self.main_container.configure(bg=self._get_colors('text_background_color'))
    
    def _get_colors(self, widget_and_option):
        return ColorManager.CODE_EDITOR_COLORS[self._appearance_mode][widget_and_option]
    
    def _create_widgets(self):
        self.main_container = tk.Frame(self, bg=self._get_colors('text_background_color'))
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
            bg=self._get_colors('line_number_background_color'),
            fg=self._get_colors('line_number_text_color'),
            relief="flat",
            border=0,
            state="disabled",
            wrap="none",
            font=(self._font),
            blockcursor=True
        )
        self.line_numbers.grid(column=0, row=1, sticky="ns")
        self._excess_frame = tk.Frame(
            self.main_container,
            width=4,
            bg=self._get_colors('line_number_background_color'),
        )
        self._excess_frame.grid(column=0,row=2, sticky="nsew")
        self._excess_frame.grid_remove()
        
        self.text_area = tk.Text(
            self.main_container,
            pady=5,
            padx=5,
            bg=self._get_colors('text_background_color'),
            fg=self._get_colors('text_color'),
            relief="flat",
            border=0,
            undo=True,
            wrap=tk.NONE,
            font=(self._font),
            insertbackground=self._get_colors('cursor_color'),
            selectbackground=self._get_colors('highlight_color'),
            selectforeground=self._get_colors('highlight_text_color')
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
            command=self.text_area.xview
        )
        self.h_scrollbar.grid(row=2,column=1, sticky= "ew")
        
        self.text_area.configure(
            yscrollcommand=self._on_text_vertical_scroll,
            xscrollcommand=self.h_scrollbar.set
        )
        
        self.line_numbers.configure(yscrollcommand=self._on_line_scroll)
        
        self._update_line_numbers()
    
    def _setup_bindings(self):
        self.text_area.bind("<KeyRelease>", self._on_text_change)
        self.text_area.bind("<Configure>", self._on_configure)
        # Enhanced key bindings
        self.text_area.bind("<Control-BackSpace>", self._ctrl_backspace)
        self.text_area.bind("<Control-Delete>", self._ctrl_delete)
        self.text_area.bind("<Control-c>", self._ctrl_c)
        self.text_area.bind("<Control-x>", self._ctrl_x)
        self.text_area.bind("<Control-C>", self._ctrl_c)
        self.text_area.bind("<Control-X>", self._ctrl_x)  
    
    def _on_vertical_scroll(self, *args):
        """Handle vertical scrolling for both text and line numbers"""
        self.text_area.yview(*args)
        self.line_numbers.yview(*args)
    
    def _on_text_vertical_scroll(self, *args):
        """Sync vertical scrollbar with text scrolling"""
        self.v_scrollbar.set(*args)
        self.line_numbers.yview_moveto(args[0])
        self._update_scrollbar_visibility()
    
    def _on_text_horizontal_scroll(self, *args):
        """Sync horizontal scrollbar with text scrolling"""
        self.h_scrollbar.set(*args)
    
    def _on_line_scroll(self, *args):
        """Sync line numbers with vertical scrolling"""
        self.v_scrollbar.set(*args)
        self.text_area.yview_moveto(args[0])
    
    def _on_text_change(self, event=None):
        self._update_line_numbers()
        self._update_scrollbar_visibility()
    
    def _update_line_numbers(self):
        current_line_count = int(self.text_area.index(self.END_MINUS_ONE_CHAR).split('.')[0])
        
        last_line_count = self._last_line_count
        
        if current_line_count == last_line_count:
            return
            
        self.line_numbers.config(state="normal")
        
        if current_line_count > last_line_count:
            new_lines = "\n".join(str(i) for i in range(last_line_count + 1, current_line_count + 1))
            if last_line_count == 0:
                # First time or complete refresh needed
                self.line_numbers.delete(self.START, tk.END)
                self.line_numbers.insert(self.START, new_lines)
            else:
                self.line_numbers.insert(tk.END, "\n" + new_lines)
        
        elif current_line_count < last_line_count:
            self.line_numbers.delete(f"{current_line_count + 1}.0", tk.END)
        
        self._last_line_count = current_line_count
        self.line_numbers.config(state="disabled")
    
    def _on_configure(self, event=None):
        """Update scrollbar visibility when widget is resized"""
        self._update_scrollbar_visibility()
    
    @debounce(timeout=0.002)
    def _update_scrollbar_visibility(self):
        """Show/hide scrollbars based on content width and height"""
        xview = self.text_area.xview()
        if xview == (0.0, 1.0):
            self.h_scrollbar.grid_remove()
            self._update_line_frame()
        else:
            self.h_scrollbar.grid()
            self._update_line_frame(True)
            
        yview = self.text_area.yview()
        if yview == (0.0, 1.0):
            self.v_scrollbar.grid_remove()
        else:
            self.v_scrollbar.grid()
            
    def _update_line_frame(self, cut=False):
        if cut:
            self._excess_frame.grid()
        else:
            self._excess_frame.grid_remove()
        
    def _replace_content(self, content):
        """Replace content of text area, preventing the program from making a separator in the undo stack"""
        self.text_area.configure(undo=False)    # prevents making a separator (undo/redo stacks) with erased content
        self.text_area.delete(self.START, tk.END)
        self.text_area.insert(self.START, content)
        self.text_area.configure(undo=True)
        
    def _move_cursor_to(self, index):
        """Move cursor to index and scroll to cursor"""
        self.text_area.mark_set(tk.INSERT, index)
        self.text_area.see(index)
        self.text_area.focus_set()

    # -------- Enhanced key bindings --------
    
    def _ctrl_backspace(self, event):
        """Delete from cursor to previous word boundary (space, special char, or start of word)"""
        cursor_position = self.text_area.index(tk.INSERT)
        line_start_index = self.text_area.index(f"{cursor_position} linestart")
        text_before_cursor = self.text_area.get(line_start_index, cursor_position)
        delete_length = 0
        if not text_before_cursor:
            delete_length = 1
        else:
            char_right_before_cursor_index = len(text_before_cursor) - 1
            line_start = 0
            for i in range(char_right_before_cursor_index, line_start-1, -1):
                if i == char_right_before_cursor_index:
                    delete_length += 1
                    continue
                
                previous_char = text_before_cursor[i + 1]
                current_char = text_before_cursor[i]
                
                if previous_char.isspace():
                    if not current_char.isspace():
                        break
                    delete_length += 1
                elif previous_char.isalnum():
                    if not current_char.isalnum():
                        break
                    delete_length += 1
                else:
                    if current_char.isspace() or current_char.isalnum():
                        break
                    delete_length += 1
        
        if delete_length > 0:
            delete_start = self.text_area.index(f"{cursor_position}-{delete_length}c")
            self.text_area.delete(delete_start, cursor_position)
            self.text_area.see(delete_start)
        
        return "break"  # prevent default behavior
    
    def _ctrl_delete(self, event):
        """Delete from cursor to next word boundary (space, special char, or end of word)"""
        cursor_position = self.text_area.index(tk.INSERT)
        line_end_index = self.text_area.index(f"{cursor_position} lineend")
        text_after_cursor = self.text_area.get(cursor_position, line_end_index)
        delete_length = 0
        if not text_after_cursor:
            delete_length = 1
        else:
            first_char = text_after_cursor[0]
            
            if first_char.isspace():
                for char in text_after_cursor:
                    if char.isspace():
                        delete_length += 1
                    else:
                        break
            else:
                if first_char.isalnum():
                    for char in text_after_cursor:
                        if char.isalnum():
                            delete_length += 1
                        else:
                            break
                else:
                    for char in text_after_cursor:
                        if not char.isspace() and not char.isalnum():
                            delete_length += 1
                        else:
                            break
        
        if delete_length > 0:
            delete_end = self.text_area.index(f"{cursor_position}+{delete_length}c")
            self.text_area.delete(cursor_position, delete_end)
        
        return "break"
    
    def _ctrl_c(self, event):
        """Enhanced Ctrl+C: if no selection, copy from cursor to end of line"""
        try:
            there_is_selection = self.text_area.tag_ranges(tk.SEL)
            if there_is_selection:
                self.text_area.event_generate("<<Copy>>")
            else:
                cursor_pos = self.text_area.index(tk.INSERT)
                line_end = self.text_area.index(f"{cursor_pos} lineend")
                text_to_copy = self.text_area.get(cursor_pos, line_end)
                
                if text_to_copy:
                    self.text_area.clipboard_clear()
                    self.text_area.clipboard_append(text_to_copy)
            
            return "break"
        except tk.TclError:
            self.text_area.event_generate("<<Copy>>")
            return "break"
    
    def _ctrl_x(self, event):
        """Enhanced Ctrl+X: if no selection, cut from cursor to end of line"""
        try:
            there_is_selection = self.text_area.tag_ranges(tk.SEL)
            if there_is_selection:
                self.text_area.event_generate("<<Cut>>")
            else:
                cursor_pos = self.text_area.index(tk.INSERT)
                line_end = self.text_area.index(f"{cursor_pos} lineend")
                text_to_cut = self.text_area.get(cursor_pos, line_end)
                
                if text_to_cut:
                    self.text_area.clipboard_clear()
                    self.text_area.clipboard_append(text_to_cut)
                    self.text_area.delete(cursor_pos, line_end)
            
            return "break"
        except tk.TclError:
            self.text_area.event_generate("<<Cut>>")
            return "break"