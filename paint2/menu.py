import customtkinter as ctk
from settings import *
from tools import *
from tkinter import colorchooser

class Menu(ctk.CTkTabview):
    def __init__(self, parent, canvas):
        super().__init__(parent, fg_color = MENU_BG_COLOR)
        self.grid(row = 0, column = 0, sticky = 'nsew', padx = 5, pady = 10)
        self.canvas = canvas

        # tabs
        self.add('Tools')
        self.add('Other')
        self.add('File')

        # Creating the different frames
        self.ToolsAndColors = ToolsAndColors(self.tab('Tools'), self.canvas)
        self.OtherTools = OtherTools(self.tab('Other'), self.canvas, self.ToolsAndColors)
        self.FileOptions = FileOptions(self.tab('File'), self.canvas)

class ToolsAndColors(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent, fg_color = 'transparent')
        self.canvas = canvas

        # Grid layout
        self.columnconfigure((0, 1, 2, 3), weight = 1, uniform = 'a')
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight = 1, uniform = 'a')

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
        self.thickness_slider = ThicknessSlider(self,
                        BRUSH_THICKNESS_SLIDER['SLIDER']['row'],
                        BRUSH_THICKNESS_SLIDER['SLIDER']['col'],
                        BRUSH_THICKNESS_SLIDER['SLIDER']['columnspan'],
                        BRUSH_THICKNESS_SLIDER['SLIDER']['max'],
                        BRUSH_THICKNESS_SLIDER['SLIDER']['min'],
                        BRUSH_THICKNESS_SLIDER['SLIDER']['default'],
                        BRUSH_THICKNESS_SLIDER['SLIDER']['button color'],
                        CURRENT_COLOR,
                        func = self.change_thickness)

        # placing
        self.pack(expand = True, fill = 'both')

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

class OtherTools(ctk.CTkFrame):
    def __init__(self, parent, canvas, tools_and_colors):
        super().__init__(parent, fg_color = 'transparent')
        self.canvas = canvas
        self.tools_and_colors = tools_and_colors

        # Grid layout
        self.columnconfigure(0, weight = 1, uniform = 'a')
        self.rowconfigure((0, 1, 2), weight = 1, uniform = 'a')

        # extra buttons
        for button, data in OTHER_OPTIONS.items():
            ExtraButton(self,
                        text = data['text'],
                        func = self.extra_func)
            
        # placing
        self.pack(expand = True, fill = 'both')

    def extra_func(self, command):
        if command == 'Clear':
            self.canvas.clear()
            self.canvas.update_image()

        if command == 'Custom Color':
            custom_color = colorchooser.askcolor(title = 'Choose Color')
            colorHex = custom_color[1]
            self.tools_and_colors.change_color(colorHex)

        if command == 'Random Image':
            self.canvas.GenerateRandomImage()

class FileOptions(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent, fg_color = 'transparent')
        self.canvas = canvas

        for button, data in FILE_OPTIONS.items():
            ExtraButton(self,
                        text = data['text'],
                        func = self.file_func)

        # placing
        self.pack(expand = True, fill = 'both')
    
    def file_func(self, command):
        if command == 'Import Image':
            self.canvas.open_dialog()
        if command == 'Export Image':
            self.canvas.Export_Image()
