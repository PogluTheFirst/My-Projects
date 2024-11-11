# Documentation

## Warning
I Know very well that a lot of code here is trash \
The menu and canvas.py documentations were done by ChatGPT, Because I'm feeling lazy \
Anyways the course where i learned tkinter like this is by Clear Code \ 
Watch it, I'm not asking

## What is it
Simple paint app with following tools:
1. Line drawing tool
2. circle drawing tool
3. square drawing tool
4. brush tool
5. bucket tool
Multiple default colors and custom color picker and clear button

## Why i made this
Made this to get more experience with tkinter and to get more used with it

## How it works

#### required modules
```txt
pip install customtkinter
pip install PIL
```

#### file structure
The code has been organized into multiple files for more readability and easier handling\
Also a lot of classes have been made for readability and handling

### Paint.py
Importing the modules
```python
import customtkinter as ctk
from paint.canvas import canvas # Module from the paint folder i made
from paint.settings import * # Module from the paint folder i made
from paint.menu import * # Module from the paint folder i made
```

```python
class PaintApp(ctk.CTk):
    super().__init__() # inherits all the functions from the class
```
main class inherits from window class of customtkinter

Setting window:
```python
self.geometry('1000x700') # app size
self.title('Simple Paint App') # app name
self.resizable(False, False) # set to false because chanigng size causes errors with bucket tool
ctk.set_appearance_mode('dark') # setting app to dark mode 
```

Grid layout for easier organization and looks
```python
self.columnconfigure(0, weight = 3, uniform = 'a')
self.columnconfigure(1, weight = 7, uniform = 'a')
self.rowconfigure(0, weight = 1)
```

Creation of menu and canvas:
```python
self.canvas = canvas(self, CURRENT_COLOR, CURRENT_TOOL, CURRENT_SLIDER_VAL) # requires extra args to work
Menu(self, self.canvas)
```

Mainloop and updating window:
```python
self.update_idletasks() # updates the window
self.mainloop()
```

### settings.py
This module includes all the colors, tools, buttons, extra settings and theirs positions and everything like that

#### Organization
Data has been organized into dictionaries for readability and easier use

### tools.py
This file contains the data required for creating the buttons
#### ColorButton
```python
class ColorButton(ctk.CTkButton): # Inherits from ctkbutton class
    def __init__(self, parent, color, hover_color, row, col, func): # all required args to create a colorbutton
        super().__init__(parent, # the container that holds this buttton
                         text = '', # set to none for no text
                         width = 75, # for some reason if i remove i height or width it colour does not fit properly
                         height = 75,
                         fg_color = color, # button background color
                         hover_color = hover_color,
                         corner_radius = 0,
                         command = lambda: func(color)) # setting the button up

        self.grid(row = row, column = col, sticky = 'nsew', padx = 5, pady = 5) # putting the button on the menu grid
```

#### ToolButton
```python
class ToolButton(ctk.CTkButton): # Inherits from ctkbutton class
    def __init__(self, parent, row, col, columnspan, text, func): # required args for creating button
        super().__init__(parent, # container of the widget
                         text = text, # button text
                         command = lambda: func(text)) # function that activates on press
        self.grid(row = row, column = col, columnspan = columnspan, sticky = 'nsew', padx = 5, pady = 5) # putting the button on the menu grid
```

#### Thickness slider
```python
class ThicknessSlider(ctk.CTkSlider): # inherits from slider class
    def __init__(self, parent, row, col, columnspan, max, min, default, button_color, button_hover_color, func): # args
        super().__init__(parent, # container of the slider
                         from_ = min, # slider minimum value
                         to = max, # slider maximum value
                         button_color = button_color, # slider button color
                         button_hover_color = button_hover_color,
                         progress_color = '#000000', # slider progress color
                         orientation = 'horizontal', # slider rotation
                         command = self.on_slider_change) # slider function that activates on slider move
    
        self.set(default) # set slider to default value from settings.py
        self.grid(row = row, column = col, columnspan = columnspan, sticky = 'ew', padx = 5, pady = 5) # placing the slider

        self.slider_value = ctk.StringVar() # adds slider value to a Variable
        self.slider_value.set(f"{int(default)}") # sets the variable to the default value

        self.slider_text = ctk.CTkLabel(parent, # text next to slider to show value
                                        textvariable = self.slider_value, # connects slider variable to text
                                        font = ('Arial', 12)) # sets font and size of text
        self.slider_text.grid(row = row, column = 3, sticky = 'nsew', padx = 5, pady = 5) # places text next to the slider

        self.external_func = func # the other function that activates on slider movement
```

Slider functions: \
Value change function:
```python
def on_slider_change(self, value): # activates when slider moves
    self.slider_value.set(f"{int(value)}") # sets the value of text to the slider value
    self.external_func(value) # activates the func that is outside the file
```

Color change function:
```python
def change_slider_color(self, color): # activates when selected color changes
    self.configure(button_color = color, button_hover_color = color) # changes the slider color
```
This color function was made as i needed a place to show the current color and used a slider rather than creating another label


#### Extra button
```python
class ExtraButton(ctk.CTkButton): # inherits from ctkbutton class
    def __init__(self, parent, text, row, col, columnspan, func): # args
        super().__init__(parent, # container that holds widget
                         text = text, # button text
                         command = lambda: func(text)) # button function
        self.grid(row = row, column = col, columnspan = columnspan, sticky = 'nsew', padx = 5, pady = 5) # placing the button
```

### menu.py
#### Overview
This documentation describes the Menu system implemented using the customtkinter library. The Menu system includes multiple tabs for different sets of functionalities like tools, file options, and other utilities. It interacts with a canvas widget to allow users to manipulate images and shapes using various tools and settings. The menu provides a user-friendly interface with options to choose colors, tools, and modify brush thickness, among others.

Menu Class
The Menu class is the main container for all menu-related options and consists of three primary tabs: Tools, Other, and File. Each tab contains specific widgets and buttons that interact with the canvas.

```python
class Menu(ctk.CTkTabview):
    def __init__(self, parent, canvas):
        super().__init__(parent, fg_color = MENU_BG_COLOR)
        self.grid(row = 0, column = 0, sticky = 'nsew', padx = 5, pady = 10)
        self.canvas = canvas

        # Tabs
        self.add('Tools')
        self.add('Other')
        self.add('File')

        # Creating the different frames
        self.ToolsAndColors = ToolsAndColors(self.tab('Tools'), self.canvas)
        self.OtherTools = OtherTools(self.tab('Other'), self.canvas, self.ToolsAndColors)
        self.FileOptions = FileOptions(self.tab('File'), self.canvas)
```
##### Parameters:
parent: The parent widget or frame in which the menu will be placed.
canvas: The canvas object that the menu will interact with.
Attributes:
ToolsAndColors: Frame containing tools and color options.
OtherTools: Frame for additional tools such as clearing the canvas or choosing a custom color.
FileOptions: Frame with file-related actions like importing and exporting images.
Tools and Colors Tab
ToolsAndColors class
This class creates a frame within the "Tools" tab that contains color buttons, tool buttons, and a brush thickness slider. It allows the user to change the active color, tool, and brush thickness.

```python
class ToolsAndColors(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent, fg_color = 'transparent')
        self.canvas = canvas
        ...
```
##### Parameters:
parent: The parent widget (in this case, the Tools tab).
canvas: The canvas object to which changes in tools and colors will be applied.
Components:
Color Buttons: A set of color buttons that change the current drawing color when clicked.
Tool Buttons: Buttons to select different tools (e.g., brush, line, circle, square).
Brush Thickness Slider: A slider to adjust the thickness of the brush for drawing.
Functions:
change_color: Updates the current color.
change_tool: Changes the selected tool.
change_thickness: Adjusts the brush thickness.
Other Tools Tab
OtherTools class
This class represents the "Other" tab and includes extra functionalities such as clearing the canvas, selecting a custom color, and generating a random image.

```python
class OtherTools(ctk.CTkFrame):
    def __init__(self, parent, canvas, tools_and_colors):
        super().__init__(parent, fg_color = 'transparent')
        self.canvas = canvas
        self.tools_and_colors = tools_and_colors
        ...
```
##### Parameters:
parent: The parent widget (in this case, the Other tab).
canvas: The canvas to manipulate.
tools_and_colors: An instance of the ToolsAndColors class.
Components:
Clear Button: Clears the canvas.
Custom Color Button: Opens a color chooser dialog to pick a custom color.
Random Image Button: Generates a random image on the canvas.
Functions:
extra_func: Handles different button commands like clearing the canvas, choosing a custom color, or generating a random image.
File Options Tab
FileOptions class
This class represents the "File" tab and provides options related to file operations, such as importing and exporting images.

```python
Copy code
class FileOptions(ctk.CTkFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent, fg_color = 'transparent')
        self.canvas = canvas
        ...
```
##### Parameters:
parent: The parent widget (in this case, the File tab).
canvas: The canvas to interact with for file operations.
Components:
Import Image Button: Opens a file dialog to select an image file and display it on the canvas.
Export Image Button: Allows the user to save the canvas as an image file.
Functions:
file_func: Handles different file-related commands like importing, exporting, and generating code documentation.
Color and Tool Management
Color Buttons
In the ToolsAndColors class, color buttons are dynamically created from the COLORS dictionary, which contains color names and their corresponding values. These buttons allow the user to select the drawing color.

Tool Buttons
Tool buttons are created from the TOOLS dictionary. Each button corresponds to a specific drawing tool, such as brush, line, circle, or square.

Thickness Slider
The brush thickness slider allows the user to adjust the thickness of the brush used for drawing. It is created using the ThicknessSlider class and is linked to the change_thickness function.

Integration with Canvas
The Menu system integrates with the canvas through functions that update the canvas based on user input:

Color Update: Changes the active color used for drawing.
Tool Update: Switches between different drawing tools.
Brush Thickness Update: Adjusts the brush size for the drawing tools.
Key Constants and Data
The following constants and data are used to configure the menu:

MENU_BG_COLOR: Background color for the menu.
COLORS: Dictionary of predefined colors for the color buttons.
TOOLS: Dictionary of tool data, including text, row, column, and other properties for each tool button.
OTHER_OPTIONS: Dictionary of additional options, such as clearing the canvas or choosing a custom color.
FILE_OPTIONS: Dictionary of file-related options like importing and exporting images.
CURRENT_COLOR, CURRENT_TOOL, CURRENT_SLIDER_VAL: Global variables that store the current color, tool, and brush thickness.
##### Summary
The Menu system allows for easy interaction with the canvas, providing options to change the color, drawing tool, and brush thickness. It also includes extra tools for clearing the canvas, selecting custom colors, and generating random images. The file options allow for importing and exporting images, making it a versatile tool for image creation and manipulation within the customtkinter framework.

#### canvas.py

##### Overview

The canvas class inherits from tkinter.Canvas and provides functionality for various drawing and image manipulation tools. The class supports features such as drawing shapes (line, square, circle), brush strokes, flood fill (bucket tool), importing and exporting images, and generating random pixel images. It is a part of a graphical user interface (GUI) built using tkinter and PIL (Python Imaging Library).

##### Methods
__init__(self, parent, current_color, current_tool, brush_thickness)
This is the initializer for the canvas class. It initializes the canvas, sets up the drawing tools, brush size, and background, and prepares the canvas for interaction.


Parameters:
parent: The parent widget to which this canvas belongs.
current_color: The color used for drawing.
current_tool: The current tool selected (Brush, Line, Circle, Square, Bucket).
brush_thickness: The thickness of the brush used for drawing.
update_color(self, new_color)
Updates the current drawing color.

Parameters:
new_color: The new color to set.
update_tool(self, new_tool)
Updates the current drawing tool.

Parameters:
new_tool: The new tool to use. Can be one of 'Brush', 'Line', 'Circle', 'Square', 'Bucket'.
update_brush_thickness(self, new_thickness)
Updates the brush thickness.

Parameters:
new_thickness: The new thickness for the brush.
Click(self, event)
Handles mouse click events on the canvas. Depending on the current tool, it performs different actions such as initiating a brush stroke, drawing a shape, or triggering a flood fill.

Parameters:
event: The mouse event containing the click position.
Drag(self, event)
Handles mouse drag events, allowing the user to draw shapes or brush strokes interactively.

Parameters:
event: The mouse event containing the drag position.
Release(self, event)
Handles mouse release events after a drawing operation. Completes the shape drawing or brush stroke.

Parameters:
event: The mouse event containing the release position.
brush_stroke(self, event_x, event_y)
Draws a brush stroke on the canvas and the image.

Parameters:
event_x: The x-coordinate of the mouse event.
event_y: The y-coordinate of the mouse event.
draw_shape(self, shape_coords, draw_on_image=False)
Draws a shape (Line, Circle, or Square) on the canvas and the image. The shape is drawn based on the given coordinates.

Parameters:

shape_coords: Coordinates for the shape to be drawn, consisting of (x1, y1, x2, y2).
draw_on_image: If True, the shape is also drawn on the image. Default is False.
Returns: The shape object created on the canvas.

bucket(self, x, y)
Handles the "Bucket" tool (flood fill). It checks the pixel color at the clicked point and replaces all contiguous pixels of the same color with the current color.

Parameters:
x: The x-coordinate where the fill operation starts.
y: The y-coordinate where the fill operation starts.
flood_fill(self, x, y, target_color, replacement_color)
Performs a flood fill operation. This function replaces all contiguous pixels of the target_color with the replacement_color.

Parameters:
x: The x-coordinate of the pixel to start the fill.
y: The y-coordinate of the pixel to start the fill.
target_color: The color to replace.
replacement_color: The color to use for replacement.
hex_to_rgb(self, hex_color)
Converts a hex color string to an RGB tuple.

Parameters:

hex_color: A color string in hexadecimal format (e.g., "#FF5733").
Returns: A tuple representing the RGB values (r, g, b).

update_image(self)
Updates the displayed image on the canvas by creating a new ImageTk.PhotoImage object and displaying it.

clear(self)
Clears the canvas and resets the image to the background color.

open_dialog(self)
Opens a file dialog to choose an image file to open.

Open_Image(self, path)
Opens an image from the specified file path and resizes it to fit the canvas dimensions.

Parameters:
path: The file path of the image to open.
Export_Image(self)
Opens a file dialog to save the current image to a specified location.

GenerateRandomImage(self)
Generates a random image by assigning random colors from a predefined palette to each pixel on the canvas.

Example Usage
```python
import tkinter as tk
from settings import BG_COLOR

root = tk.Tk()
canvas = canvas(root, current_color="#FF0000", current_tool="Brush", brush_thickness=5)

# Set up canvas with a random image
canvas.GenerateRandomImage()

# Open an image
canvas.open_dialog()

# Export the current image
canvas.Export_Image()

root.mainloop()
```
Palette of Colors
The GenerateRandomImage method uses a predefined palette of 64 colors, including variations of grays, reds, oranges, yellows, greens, cyan, blues, and purples. You can modify or extend this palette to fit your needs.

# The end