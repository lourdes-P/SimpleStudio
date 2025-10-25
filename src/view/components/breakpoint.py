import tkinter as tk
from dataclasses import dataclass
from view.utils.color_manager import ColorManager

@dataclass
class Breakpoint:
    x: int
    y: int
    address: str
    radius: int = 4
    active: bool = False
    fill_on: str = ColorManager.BREAKPOINT_COLOR
    fill_off: str = ''
    fill_hover: str = ColorManager.HOVER_BREAKPOINT_COLOR
    hover: bool = False

    def contains(self, px: int, py: int) -> bool:
        return (px - self.x) ** 2 + (py - self.y) ** 2 <= (self.radius + 2) ** 2


class BreakpointCanvas(tk.Canvas):
    def __init__(self, master=None, width=300, height=200, on_breakpoint_click_callback=None, **kwargs):
        super().__init__(master, width=width, height=height, highlightthickness=0, **kwargs)
        self.breakpoints: list[Breakpoint] = []
        self.items_map = {}  # canvas_id -> Breakpoint
        self._on_breakpoint_click_callback = on_breakpoint_click_callback
        self.bind("<Button-1>", self._on_click)
        self.bind("<Motion>", self._on_motion)
        self.bind("<Leave>", self._on_leave)

    def add_breakpoint(self, x=None, y=None, address=None, active=False, breakpoint: Breakpoint=None):
        """If breakpoint is None, creates a new Breakpoint with the rest of the arguments (which then are all MANDATORY), and appends it to the breakpoint list"""
        if breakpoint is None:
            breakpoint = Breakpoint(x=x, y=y, address=address, active=active)
        self.breakpoints.append(breakpoint)
        self._draw_one(breakpoint)

    def _draw_one(self, breakpoint: Breakpoint):
        r = breakpoint.radius
        x, y = breakpoint.x, breakpoint.y
        
        if breakpoint.active:
            fill_color = breakpoint.fill_on
        elif breakpoint.hover:
            fill_color = breakpoint.fill_hover
        else:
            fill_color = breakpoint.fill_off

        circle = self.create_oval(x - r, y - r, x + r, y + r, fill=fill_color, outline='',)
        
        self.items_map[circle] = breakpoint

    def redraw(self):
        self.delete("all")
        self.items_map.clear()
        for breakpoint in self.breakpoints:
            self._draw_one(breakpoint)

    def clear(self):
        self.delete("all")
        self.items_map.clear()
        self.breakpoints.clear()

    def _on_click(self, event):
        items = self.find_overlapping(event.x-2, event.y-2, event.x+2, event.y+2)
        for iid in items:
            breakpoint = self.items_map.get(iid)
            if breakpoint:
                breakpoint.active = not breakpoint.active
                self.redraw()
                self._on_breakpoint_click_callback(breakpoint.address)
                return

    def _on_motion(self, event):
        hover_found_over_breakpoint = False
        for breakpoint in self.breakpoints:
            old_hover = breakpoint.hover
            breakpoint.hover = breakpoint.contains(event.x, event.y)
            if old_hover != breakpoint.hover:
                self.redraw()
            if breakpoint.hover:
                hover_found_over_breakpoint = True
        
        if hover_found_over_breakpoint:
            self.config(cursor="hand2")
        else:
            self.config(cursor="")

    def _on_leave(self, event):
        for breakpoint in self.breakpoints:
            if breakpoint.hover:
                breakpoint.hover = False
                self.redraw()
        self.config(cursor="")