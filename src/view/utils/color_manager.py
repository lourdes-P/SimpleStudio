import os
from customtkinter import ThemeManager
import customtkinter as ctk

class ColorManager:
    SECONDARY_COLOR = ("#325b83",'#2c3e50')
    TERTIARY_COLOR = ("#86a7c7", "#86a7c7")
    BREAKPOINT_COLOR = '#c4160a'
    HOVER_BREAKPOINT_COLOR = ("#c49292","#680b05")
    CODE_EDITOR_COLORS = {  
                          'Dark':
                              {
                                'cursor_color': "#CCCCCC",
                                'text_background_color': "#2b2b2b",
                                'text_color': "white",
                                'line_number_background_color': "#3c3c3c",
                                'line_number_text_color': "#8A8A8A",
                                'highlight_color':"#366693",
                                'highlight_text_color': 'white',
                              },
                          'Light':
                              {
                                'cursor_color': "#363636",
                                'text_background_color': "#e6e6e6",
                                'text_color': "black",
                                'line_number_background_color': "#d4d4d4",
                                'line_number_text_color': "#585858",
                                'highlight_color':"#B2D3F3",
                                'highlight_text_color': 'black',
                              }
                         }
    
    @staticmethod
    def get_secondary_color():
        return ColorManager.get_single_color(ColorManager.SECONDARY_COLOR)
        
    @staticmethod
    def get_tertiary_color():
        return ColorManager.get_single_color(ColorManager.TERTIARY_COLOR)
    
    @staticmethod
    def get_alternating_colors(widget, index: int):
        """Get the background color for alternating rows.
        If color is transparent, it will get the color from the parent of the widget."""
        header_color = 'transparent'
        if index % 2 != 0:
            header_color = ColorManager.get_single_color(widget._fg_color)
            if header_color is None:
                header_color = ColorManager.get_single_color(ThemeManager.theme["CTkFrame"]["fg_color"])
        
        if header_color == 'transparent':      
            header_color = ColorManager.get_non_transparent_color(widget.master, header_color)
        return header_color
    
    @staticmethod         
    def get_single_color(color_tuple, appearance_mode = None):
        """Convert CTk color tuple to single color string based on current appearance mode"""
        if appearance_mode is None:
            appearance_mode = ctk.get_appearance_mode()
            
        if appearance_mode == "Light":
            return color_tuple[0]  
        else:
            return color_tuple[1]
        
    @staticmethod
    def get_text_color(widget):
        return widget.cget("text_color")
    
    @staticmethod
    def get_theme_background_color(widget):
        return ColorManager.get_single_color(widget.cget("fg_color"))
    
    @staticmethod
    def get_theme_text_color():
        label = ctk.CTkLabel(None)
        text_color = label.cget("text_color")
        label.destroy()
        return ColorManager.get_single_color(text_color)
    
    @staticmethod
    def get_non_transparent_color(widget, color):
        if color == "transparent":
            try:
                color = ColorManager.get_single_color(widget.cget("fg_color"))
            except:
                if ctk.get_appearance_mode().lower() == "dark":
                    color = "#2b2b2b"  
                else:
                    color = "#f0f0f0"  
        return color