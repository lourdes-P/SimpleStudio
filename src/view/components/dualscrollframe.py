import customtkinter as ctk
import tkinter as tk

from view.utils.color_manager import ColorManager

class DualScrollFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Create canvas and scrollbars
        self.canvas = tk.Canvas(self, highlightthickness=0, bg=ColorManager.get_single_color(self._fg_color))
        
        self.h_scrollbar = ctk.CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview)
        self.v_scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color=ColorManager.get_single_color(self._fg_color), corner_radius=0)
        self.scrollable_frame.pack(fill="both", expand=True)
  
        ctk.AppearanceModeTracker.add(self.change_appearance_mode)
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        
        # Grid layout
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")        
        
        self.set_bindings()
        
    def set_scrollable_frame(self, frame):
        self.scrollable_frame.destroy()
        self.scrollable_frame= frame
        #self.scrollable_frame.pack(fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.set_bindings()
        
    def set_canvas(self, canvas):
        self.canvas = canvas
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color=ColorManager.get_single_color(self._fg_color), corner_radius=0)
        self.scrollable_frame.pack(fill="both", expand=True)
        self.canvas_window.destroy()
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.set_bindings()
    
    def set_bindings(self):
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        self.canvas.bind("<Enter>", lambda e: self.bind_mousewheel())
        self.canvas.bind("<Leave>", lambda e: self.unbind_mousewheel())
        
    def on_frame_configure(self, event):
        """Update scrollregion when the size of the inner frame changes"""
        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.configure(scrollregion=bbox)
        self.update_scrollbars()
        
    def on_canvas_configure(self, event):
        self.update_scrollbars()
        
    def update_scrollbars(self):
        """Show or hide scrollbars based on content size"""
        # Get the bounding box of all items in the canvas
        bbox = self.canvas.bbox("all")
        if bbox is None:
            return
            
        # Calculate content width and height
        content_width = bbox[2] - bbox[0]
        content_height = bbox[3] - bbox[1]
        
        # Get canvas current dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Show/hide vertical scrollbar
        if content_height > canvas_height:
            self.v_scrollbar.grid()
        else:
            self.v_scrollbar.grid_remove()
            
        # Show/hide horizontal scrollbar
        if content_width > canvas_width:
            self.h_scrollbar.grid()
        else:
            self.h_scrollbar.grid_remove()
        
    def bind_mousewheel(self):
        """Bind mousewheel events for scrolling"""
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self.on_shift_mousewheel)
        
    def unbind_mousewheel(self):
        """Unbind mousewheel events"""
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Shift-MouseWheel>")
        
    def on_mousewheel(self, event):
        """Vertical scrolling with mousewheel"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
    def on_shift_mousewheel(self, event):
        """Horizontal scrolling with shift+mousewheel"""
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
        
    def change_appearance_mode(self, mode=None):
        fg_color = ColorManager.get_single_color(self._fg_color)
        self.canvas.configure(bg=fg_color)
        self.scrollable_frame.configure(fg_color=fg_color)      
        
    def get_scrollable_frame(self):
        return self.scrollable_frame