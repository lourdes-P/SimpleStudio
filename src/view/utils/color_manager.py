from customtkinter import ThemeManager
import customtkinter as ctk

class ColorManager:
    SECONDARY_COLOR = '#2c3e50'
    TERTIARY_COLOR = '#4b8bab'
    BREAKPOINT_COLOR = '#c4160a'
    
    @staticmethod
    def get_alternating_colors(parent, index: int):
        """Get the background color for alternating rows"""
        header_color = 'transparent'
        if index % 2 != 0:
            header_color = ColorManager.get_single_color(parent._fg_color)
            if header_color is None:
                header_color = ColorManager.get_single_color(ThemeManager.theme["CTkFrame"]["fg_color"])
        return header_color
    
    @staticmethod         
    def get_single_color(color_tuple):
        """Convert CTk color tuple to single color string based on current appearance mode"""
        if ctk.get_appearance_mode().lower() == "light":
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
        
            