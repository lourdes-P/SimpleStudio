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
    fill_hover: str = "#ffcccc"  # Light red for hover
    outline: str = ''
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

    def add_breakpoint(self, bp: Breakpoint):
        self.breakpoints.append(bp)
        self._draw_one(bp)

    def _draw_one(self, bp: Breakpoint):
        r = bp.radius
        x, y = bp.x, bp.y
        # Determine fill color based on state
        if bp.active:
            fill = bp.fill_on
        elif bp.hover:
            fill = bp.fill_hover
        else:
            fill = bp.fill_off

        circle = self.create_oval(x - r, y - r, x + r, y + r, fill=fill, outline='',)
        
        self.items_map[circle] = bp

    def redraw(self):
        self.delete("all")
        self.items_map.clear()
        for bp in self.breakpoints:
            self._draw_one(bp)

    def clear(self):
        self.delete("all")
        self.items_map.clear()
        self.breakpoints.clear()

    def _on_click(self, event):
        items = self.find_overlapping(event.x-2, event.y-2, event.x+2, event.y+2)
        for iid in items:
            bp = self.items_map.get(iid)
            if bp:
                bp.active = not bp.active
                self.redraw()
                self._on_breakpoint_click_callback(bp.address)
                return

    def _on_motion(self, event):
        hover_found = False
        for bp in self.breakpoints:
            old_hover = bp.hover
            bp.hover = bp.contains(event.x, event.y)
            if old_hover != bp.hover:
                self.redraw()
            if bp.hover:
                hover_found = True
        
        # Change cursor to hand when hovering over breakpoints
        if hover_found:
            self.config(cursor="hand2")
        else:
            self.config(cursor="")

    def _on_leave(self, event):
        for bp in self.breakpoints:
            if bp.hover:
                bp.hover = False
                self.redraw()
        self.config(cursor="")