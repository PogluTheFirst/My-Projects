# Documentation

## Warning
Insane amount of Spaghetti code coming up
I only realized it after seeing it now
I still don't know why i made it like this

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
This file contains the logic of the menu and the tools inside it
```python
import customtkinter as ctk
from paint.settings import * # importing the settings of the tools
from paint.tools import * # importing tools
from tkinter import colorchooser # tkinter file that allows to choose custom colors
```

```python
class Menu(ctk.CTkFrame): # Inherits from ctkFrame class
    def __init__(self, parent, canvas): # args
        super().__init__(parent, bg_color = MENU_BG_COLOR, fg_color = MENU_BG_COLOR) # setting background and foreground color
        self.grid(row = 0, column = 0, sticky = 'nsew', padx = 5, pady = 10) # placing the menu
        self.canvas = canvas # initializing the canvas in the menu for later functions
```

Grid layout has been used for easiness and looks
```python
self.columnconfigure((0, 1, 2, 3), weight = 1, uniform = 'a') # 4 columns
self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight = 1, uniform = 'a') # 10 rows
```

All the tools have been created through loops so that i dont have to make every tool seperately
Data in dictionaries allows for easier sorting and readability

Color buttons:
```python
for color, data in COLORS.items(): # for loop that takes the color and data of the color for the dict in settings.py
    ColorButton(self, # container that holds the widget
                color = data['Color'], # the color of the button
                hover_color = data['hover_color'], # color that appears when hovering over the color
                row = data['row'], # row that the color is placed in
                col = data['col'], # column that the color is placed in
                func = self.change_color) # function that activates on clicking the color
```

Tool buttons:
```python
for button, data in TOOLS.items(): # takes the tool and tool data from dict
    ToolButton(self, # container of the tool
               row = data['row'], # row that the tool is placed in
               col = data['col'], # column that tool is placed in
               columnspan = data['columnspan'], # how much of the column the tool takes up
               text = data['text'], # text of the tool
               func = self.change_tool) # function that activates on press
```

Slider and slider text:
```python
self.thickness_slider = ThicknessSlider(self, # container that holds slider and slider text
    BRUSH_THICKNESS_SLIDER['SLIDER']['row'], # row of the slider and the text
    BRUSH_THICKNESS_SLIDER['SLIDER']['col'], # column of the slider and the text
    BRUSH_THICKNESS_SLIDER['SLIDER']['columnspan'], # column area that slider takes up
    BRUSH_THICKNESS_SLIDER['SLIDER']['max'], # maximum slider value
    BRUSH_THICKNESS_SLIDER['SLIDER']['min'], # minimum slider value
    BRUSH_THICKNESS_SLIDER['SLIDER']['default'], # slider default value
    BRUSH_THICKNESS_SLIDER['SLIDER']['button color'], # setting the buttton color
    CURRENT_COLOR, # slider hover color that appears when hovering over the slider button
    func = self.change_thickness) # slider func
```

Extra buttons:
```python
for button, data in EXTRA.items(): # grabs the button and its data from the dict in settings.py
    ExtraButton(self, # container holding the items
                text = data['text'], # text of the button
                row = data['row'], # row of the button
                col = data['col'], # column of the button
                columnspan = data['columnspan'], # how many columns button takes
                func = self.extra_func) # function of the button
```

Menu functions: \
Change color
```python
def change_color(self, color): # changes the current brush color
    global CURRENT_COLOR # gets the global color so that it also changes in the canvas
    CURRENT_COLOR = color # changes the color
    self.thickness_slider.change_slider_color(color) # changes the slider button color
    self.canvas.update_color(color) # updates color in the canvas
```

Change tool
```python
def change_tool(self, tool): # changes the current tool
    global CURRENT_TOOL # gets the global tool so that it also changes in the canvas
    CURRENT_TOOL = tool # changes the tool
    self.canvas.update_tool(tool) # updates the tool in canvas
```

Change thickness
```python
def change_thickness(self, thickness): # changes the brush thickness
    global CURRENT_SLIDER_VAL # gets the global thickness value
    CURRENT_SLIDER_VAL = thickness # changes the thickness
    self.canvas.update_brush_thickness(thickness) # updates the thickness in the canvas
```

Extra func
```python
def extra_func(self, command): # does the function of the extra button
    if command == 'Clear': # checks if clear button is clicked
        self.canvas.clear() # clears the canvas
        self.canvas.update_image() # updates the canvas
    
    if command == 'Custom Color': # checks if custom color button is clicked
        custom_color = colorchooser.askcolor(title = 'Choose Color') # pulls the color chooser window
        colorHex = custom_color[1] # takes the hex code of the chosen value
        self.change_color(colorHex) # calls the change color func with the chosen color
```

#### canvas.py
This file contains the entire drawing logic \
Used modules:
```python
from tkinter import Canvas
from PIL import Image, ImageDraw, ImageTk # image manipulation tools from pillow module
from paint.settings import *
```

```python
class canvas(Canvas): # inherits from tkinter canvas class
    def __init__(self, parent, current_color, current_tool, brush_thickness): # args
        super().__init__(parent, bg=BG_COLOR, highlightthickness=0) # setting color
        self.grid(row=0, column=1, sticky='nsew', padx=20, pady=30) # placing the canvas
        self.update_idletasks() # updating the canvas
```

Variables and binds:
```python
self.clicked_x, self.clicked_y = None, None # coordinates where clicked
self.current_color = current_color # current color selected
self.current_tool = current_tool # current tool selected
self.brush_thickness = brush_thickness # brush thickness
self.current_shape = None # current shape selected

self.image = Image.new('RGB', # creating an image on the canvas in the rgb color format
                       (self.winfo_width(), self.winfo_height()), # setting image to canvas width and height
                       BG_COLOR) # setting image to canvas bg_color
self.draw = ImageDraw.Draw(self.image) # drawing the image

self.update_image() # updating the image

self.bind('<Button-1>', self.Click) # func activates on click
self.bind('<B1-Motion>', self.Drag) # func that activates on clicking and dragging at the same time
self.bind('<ButtonRelease-1>', self.Release) # func that activates on release of mouse
```

Update functions:
```python
def update_color(self, new_color): # this functions updates the color
    self.current_color = new_color

def update_tool(self, new_tool): # updates the tool
    self.current_tool = new_tool

def update_brush_thickness(self, new_thickness): # updates brush thickness
    self.brush_thickness = new_thickness

def update_image(self): # updates the image
    self.canvas_image = ImageTk.PhotoImage(self.image) # recreates the current image on the screen as base image
    self.create_image(0, 0, image=self.canvas_image, anchor='nw') # places the new image
```

Clear method:
```python
def clear(self):
    self.delete('all') # deletes everything from canvas
    
    self.image = Image.new('RGB', # creates new fresh image in rgb color format
                           (self.winfo_width(), self.winfo_height()), # sets image height and width
                           BG_COLOR) # sets image color
    self.draw = ImageDraw.Draw(self.image) # draws the image
    
    self.configure(bg = BG_COLOR) # changes canvas bg_color to default
    self.update_image() # updates the image
```

Converting hex to rgb:
```python
def hex_to_rgb(self, hex_color):
    hex_color = hex_color.lstrip('#') # removes # from the hexcode
    
    rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4)) # converts it to rgb
    
    return rgb # returns it
```

Click:
```python
def Click(self, event):
    self.clicked_x, self.clicked_y = event.x, event.y # coordinates where you clicked
    
    if self.current_tool == 'Brush': # checks current tool
        self.brush_stroke(event.x, event.y) # activates brush stroke function
    
    if self.current_tool in ('Line', 'Circle', 'Square'): # checks if tool is line circle or square
        self.shape_coords = (self.clicked_x, self.clicked_y, event.x, # sets the coords of the shape
                             event.y)
        self.current_shape = None # sets the current shape
    
    if self.current_tool == 'Bucket': # checks current tool
        self.bucket(event.x, event.y) # activates the bucket function
```

Drag:
```python
def Drag(self, event):
    if self.current_tool == 'Brush': # checks if tool is brush
        self.brush_stroke(event.x, event.y) # makes a brush stroke
    
    if self.current_tool in ('Line', 'Circle', 'Square'): # checks if current tool is line circle or square
        if self.current_shape: # checks if there is a previous shape during the drag function
            self.delete(self.current_shape) # deletes that previous shape to draw new one to give dragging animation
    
        self.shape_coords = (self.clicked_x, self.clicked_y, event.x, event.y) # sets new shape coords
    
        self.current_shape = self.draw_shape(self.shape_coords, draw_on_image=False) # creates the shape
```

Release:
```python
def Release(self, event):
    self.shape_coords = (self.clicked_x, self.clicked_y, event.x, event.y) # finalizes the shape coords
    
    if self.current_shape: # checks if that shape has any previous iteration
        self.delete(self.current_shape) # deletes previous shape
    
    self.draw_shape(self.shape_coords, draw_on_image=True) # creates the final shape
    self.update_image() # updates the image
```

Brush stroke function:
```python
def brush_stroke(self, event_x, event_y):
    self.create_oval(event_x - self.brush_thickness, # creates brush stroke with the coordinates
                     event_y - self.brush_thickness, # coordinate for brush stoke
                     event_x + self.brush_thickness, # coordinate for brush stoke
                     event_y + self.brush_thickness, # coordinate for brush stoke
                     fill=self.current_color, # fills it with color
                     outline=self.current_color) # sets outline to the current color
    self.draw.ellipse([ # draws the shape on the image rather than the canvas
        event_x - self.brush_thickness, event_y - self.brush_thickness,
        event_x + self.brush_thickness, event_y + self.brush_thickness
    ],
                      fill=self.current_color)
    self.update_image() # updates the image
```

Drawing the shapes:
```python
def draw_shape(self, shape_coords, draw_on_image = False):
    x1, y1, x2, y2 = shape_coords # initializes shape coords

    # following for lines are required to stop a PIL library error where x0 or y0 is less than x1 or y1 
    top_left_x = min(x1, x2) # takes minimum from x1 and x2
    top_left_y = min(y1, y2) # takes minimum from y1 and y2
    bottom_right_x = max(x1, x2) # takes maximum from x1 and x2
    bottom_right_y = max(y1, y2) # takes maximum from y1 and y2
    
    shape = None # sets currents shape
    
    if self.current_tool == 'Line': # if tool is line
        shape = self.create_line(x1, y1, x2, y2, # coords
                                 fill=self.current_color, # color
                                 width=int(self.brush_thickness)) # width
    
        if draw_on_image: # if draw on image is true
            self.draw.line([x1, y1, x2, y2], # creates a line on the image
                           fill=self.current_color,
                           width=int(self.brush_thickness))
    
    elif self.current_tool == 'Square': # if tool is square
        shape = self.create_rectangle(top_left_x, top_left_y, bottom_right_x, bottom_right_y, # coords
                                      width=int(self.brush_thickness), # width
                                      outline=self.current_color) # outline
    
        if draw_on_image: # draws the rectangle on the image and not the canvas
            self.draw.rectangle([top_left_x, top_left_y, bottom_right_x, bottom_right_y],
                                outline=self.current_color,
                                width=int(self.brush_thickness))
    
    elif self.current_tool == 'Circle': # if tool is circle
        shape = self.create_oval(top_left_x, top_left_y, bottom_right_x, bottom_right_y, # coords
                                 width=int(self.brush_thickness), # width
                                 outline=self.current_color) # outline
    
        if draw_on_image: # creates shape on the image and not the canvas
            self.draw.ellipse([top_left_x, top_left_y, bottom_right_x, bottom_right_y],
                              outline=self.current_color,
                              width=int(self.brush_thickness))
    
    return shape # returns the created image
```

Bucket function:
```python
def bucket(self, x, y):
    pixels = self.image.load() # loads the pixels
    target_color = pixels[x, y] # takes the color of the clicked pixel as a variable
    width, height = self.image.size # gets image size
    rgb = self.hex_to_rgb(self.current_color) # converts current current color to rgb
    
    if not (0 <= x < width and 0 <= y < height): # checks if click is in the image
        return # exits function
    
    if target_color == rgb: # checks if clicked pixel color is equal to current color
        return # exits function
    
    self.flood_fill(x, y, target_color, rgb) # runs the flood fill algorithm 
    self.update_image() # updates the image
```

Flood fill algorithm:
```python
def flood_fill(self, x, y, target_color, replacement_color):
    width, height = self.image.size # gets the image heigh and width
    if not (0 <= x < width and 0 <= y < height): # checks if click is in the image
        return # exits the funciton
    
    pixels = self.image.load() # loads the pixels
    if pixels[x, y] != target_color: # checks if clicked pixel color is not equal to the target_color, target_color is the color clicked
        return # exits function
    if target_color == replacement_color: # checks if clicked pixels is equal to the replacement color
        return # exits the function
    
    stack = [(x, y)] # creates the stack which is a list of pixels
    while stack: # if the stack has elements in it runs the loop
        x, y = stack.pop() # removes the current element from the stack
        if not (0 <= x < width and 0 <= y < height): # checks if the pixels is in the image
            continue # exits this iteration of the loop
    
        if pixels[x, y] == target_color: # check if pixel color is equal to target color
            pixels[x, y] = replacement_color # replaces the pixel color to current color
    
            stack.append((x + 1, y)) # adds right pixel to the stack
            stack.append((x - 1, y)) # adds left pixel to the stack
            stack.append((x, y + 1)) # adds bottom pixel to the stack
            stack.append((x, y - 1)) # adds top pixel to the stack
    
    self.update_image() # updates the image
```
flood fill algorithm uses a stack to avoid getting a recursion error stack is a list of pixels to visit

Documenting is kinda boring
This is over 500 lines of documentation
well then, without further ado

# The end
