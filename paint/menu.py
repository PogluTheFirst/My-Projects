import customtkinter as ctk
from paint.settings import *
from paint.tools import *
from tkinter import colorchooser

class Menu(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent, bg_color = MENU_BG_COLOR, fg_color = MENU_BG_COLOR)
        self.grid(row = 0, column = 0, sticky = 'nsew', padx = 5, pady = 10)
        self.canvas = canvas

        # divide
        self.columnconfigure((0, 1, 2, 3), weight = 1, uniform = 'a')
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight = 1, uniform = 'a')
    
        # color buttons
        for color, data in COLORS.items():
            ColorButton(self, 
                        color = data['Color'],
                        hover_color = data['hover_color'],
                        row = data['row'],
                        col = data['col'],
                        func = self.change_color)
            
        # tool buttons
        for button, data in TOOLS.items():
            ToolButton(self,
                       row = data['row'],
                       col = data['col'],
                       columnspan = data['columnspan'],
                       text = data['text'],
                       func = self.change_tool)

        # slider and text
        self.thickness_slider =ThicknessSlider(self,
                        BRUSH_THICKNESS_SLIDER['SLIDER']['row'],
                        BRUSH_THICKNESS_SLIDER['SLIDER']['col'],
                        BRUSH_THICKNESS_SLIDER['SLIDER']['columnspan'],
                        BRUSH_THICKNESS_SLIDER['SLIDER']['max'],
                        BRUSH_THICKNESS_SLIDER['SLIDER']['min'],
                        BRUSH_THICKNESS_SLIDER['SLIDER']['default'],
                        BRUSH_THICKNESS_SLIDER['SLIDER']['button color'],
                        CURRENT_COLOR,
                        func = self.change_thickness)
            
        # extra options buttons
        for button, data in EXTRA.items():
            ExtraButton(self,
                        text = data['text'],
                        row = data['row'],
                        col = data['col'],
                        columnspan = data['columnspan'],
                        func = self.extra_func)

    def change_color(self, color):
        global CURRENT_COLOR
        CURRENT_COLOR = color
        self.thickness_slider.change_slider_color(color)
        self.canvas.update_color(color)
     

    def change_tool(self, tool):
        global CURRENT_TOOL
        CURRENT_TOOL = tool
        self.canvas.update_tool(tool)

    def change_thickness(self, thickness):
        global CURRENT_SLIDER_VAL
        CURRENT_SLIDER_VAL = thickness
        self.canvas.update_brush_thickness(thickness)
    
    def extra_func(self, command):
        if command == 'Clear':
            self.canvas.clear()
            self.canvas.update_image()

        if command == 'Custom Color':
            custom_color = colorchooser.askcolor(title = 'Choose Color')
            colorHex = custom_color[1]
            self.change_color(colorHex)