import customtkinter as ctk
from settings import *

class ColorButton(ctk.CTkButton):
    def __init__(self, parent, color, hover_color, row, col, func):
        super().__init__(parent,
                         text = '',
                         width = 65, # for some reason if i remove i height or width it colour does not fit properly
                         height = 65,
                         fg_color = color,
                         hover_color = hover_color,
                         corner_radius = 0,
                         command = lambda: func(color))
        self.grid(row = row, column = col, sticky = 'nsew', padx = 5, pady = 5)

class ToolButton(ctk.CTkButton):
    def __init__(self, parent, row, col, columnspan, text, func):
        super().__init__(parent,
                         text = text,
                         command = lambda: func(text))
        self.grid(row = row, column = col, columnspan = columnspan, sticky = 'nsew', padx = 5, pady = 5)

class ThicknessSlider(ctk.CTkSlider):
    def __init__(self, parent, row, col, columnspan, max, min, default, button_color, button_hover_color, func):
        super().__init__(parent,
                         from_ = min,
                         to = max,
                         button_color = button_color,
                         button_hover_color = button_hover_color,
                         progress_color = '#000000',
                         orientation = 'horizontal',
                         command = self.on_slider_change)
        
        self.set(default)
        self.grid(row = row, column = col, columnspan = columnspan, sticky = 'ew', padx = 5, pady = 5)

        self.slider_value = ctk.StringVar()
        self.slider_value.set(f"{int(default)}")

        self.slider_text = ctk.CTkLabel(parent,
                                        textvariable = self.slider_value,
                                        font = ('Arial', 12))
        self.slider_text.grid(row = row, column = 3, sticky = 'nsew', padx = 5, pady = 5)

        self.external_func = func

    def on_slider_change(self, value):
        self.slider_value.set(f"{int(value)}")
        self.external_func(value)

    def change_slider_color(self, color):
        self.configure(button_color = color, button_hover_color = color)

class ExtraButton(ctk.CTkButton):
    def __init__(self, parent, text, func):
        super().__init__(parent,
                         text = text,
                         height = 45,
                         command = lambda: func(text))
        self.pack(fill = 'x', anchor = 'n', padx = 10, pady = 5)
