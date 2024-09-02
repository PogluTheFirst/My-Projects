from tkinter import Canvas
from PIL import Image, ImageDraw, ImageTk
from paint.settings import *


class canvas(Canvas):
    def __init__(self, parent, current_color, current_tool, brush_thickness):
        super().__init__(parent, bg=BG_COLOR, highlightthickness=0)
        self.grid(row=0, column=1, sticky='nsew', padx=20, pady=30)

        self.update_idletasks()
        self.clicked_x, self.clicked_y = None, None
        self.current_color = current_color
        self.current_tool = current_tool
        self.brush_thickness = brush_thickness
        self.current_shape = None

        self.image = Image.new('RGB',
                               (self.winfo_width(), self.winfo_height()),
                               BG_COLOR)
        self.draw = ImageDraw.Draw(self.image)

        self.update_image()

        self.bind('<Button-1>', self.Click)
        self.bind('<B1-Motion>', self.Drag)
        self.bind('<ButtonRelease-1>', self.Release)

    def update_color(self, new_color):
        self.current_color = new_color

    def update_tool(self, new_tool):
        self.current_tool = new_tool

    def update_brush_thickness(self, new_thickness):
        self.brush_thickness = new_thickness

    def Click(self, event):
        self.clicked_x, self.clicked_y = event.x, event.y

        if self.current_tool == 'Brush':
            self.brush_stroke(event.x, event.y)

        if self.current_tool in ('Line', 'Circle', 'Square'):
            self.shape_coords = (self.clicked_x, self.clicked_y, event.x,
                                 event.y)
            self.current_shape = None

        if self.current_tool == 'Bucket':
            self.bucket(event.x, event.y)

    def Drag(self, event):
        if self.current_tool == 'Brush':
            self.brush_stroke(event.x, event.y)
        
        if self.current_tool in ('Line', 'Circle', 'Square'):
            if self.current_shape:
                self.delete(self.current_shape)

            self.shape_coords = (self.clicked_x, self.clicked_y, event.x, event.y)

            self.current_shape = self.draw_shape(self.shape_coords, draw_on_image=False)

    def Release(self, event):
        self.shape_coords = (self.clicked_x, self.clicked_y, event.x, event.y)

        if self.current_shape:
            self.delete(self.current_shape)

        self.draw_shape(self.shape_coords, draw_on_image=True)
        self.update_image()  


    def brush_stroke(self, event_x, event_y):
        self.create_oval(event_x - self.brush_thickness,
                         event_y - self.brush_thickness,
                         event_x + self.brush_thickness,
                         event_y + self.brush_thickness,
                         fill=self.current_color,
                         outline=self.current_color)
        self.draw.ellipse([
            event_x - self.brush_thickness, event_y - self.brush_thickness,
            event_x + self.brush_thickness, event_y + self.brush_thickness
        ],
                          fill=self.current_color)
        self.update_image()

    def draw_shape(self, shape_coords, draw_on_image = False):
        x1, y1, x2, y2 = shape_coords

        top_left_x = min(x1, x2)
        top_left_y = min(y1, y2)
        bottom_right_x = max(x1, x2)
        bottom_right_y = max(y1, y2)

        shape = None

        if self.current_tool == 'Line':
            shape = self.create_line(x1, y1, x2, y2,
                                     fill=self.current_color,
                                     width=int(self.brush_thickness))

            if draw_on_image:
                self.draw.line([x1, y1, x2, y2],
                               fill=self.current_color,
                               width=int(self.brush_thickness))

        elif self.current_tool == 'Square':
            shape = self.create_rectangle(top_left_x, top_left_y, bottom_right_x, bottom_right_y,
                                          width=int(self.brush_thickness),
                                          outline=self.current_color)

            if draw_on_image:
                self.draw.rectangle([top_left_x, top_left_y, bottom_right_x, bottom_right_y],
                                    outline=self.current_color,
                                    width=int(self.brush_thickness))

        elif self.current_tool == 'Circle':
            shape = self.create_oval(top_left_x, top_left_y, bottom_right_x, bottom_right_y,
                                     width=int(self.brush_thickness),
                                     outline=self.current_color)

            if draw_on_image:
                self.draw.ellipse([top_left_x, top_left_y, bottom_right_x, bottom_right_y],
                                  outline=self.current_color,
                                  width=int(self.brush_thickness))

        return shape

    def bucket(self, x, y):
        pixels = self.image.load()
        target_color = pixels[x, y]
        width, height = self.image.size
        rgb = self.hex_to_rgb(self.current_color)

        if not (0 <= x < width and 0 <= y < height):
            return

        if target_color == rgb:
            return

        self.flood_fill(x, y, target_color, rgb)
        self.update_image()

    def flood_fill(self, x, y, target_color, replacement_color):
        width, height = self.image.size
        if not (0 <= x < width and 0 <= y < height):
            return

        pixels = self.image.load()
        if pixels[x, y] != target_color:
            return
        if target_color == replacement_color:
            return
            
        stack = [(x, y)]
        while stack:
            x, y = stack.pop()
            if not (0 <= x < width and 0 <= y < height):
                continue

            if pixels[x, y] == target_color:
                pixels[x, y] = replacement_color

                stack.append((x + 1, y))
                stack.append((x - 1, y))
                stack.append((x, y + 1))
                stack.append((x, y - 1))

        self.update_image()

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')

        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

        return rgb

    def update_image(self):
        self.canvas_image = ImageTk.PhotoImage(self.image)
        self.create_image(0, 0, image=self.canvas_image, anchor='nw')

    def clear(self):
        self.delete('all')

        self.image = Image.new('RGB',
                               (self.winfo_width(), self.winfo_height()),
                               BG_COLOR)
        self.draw = ImageDraw.Draw(self.image)

        self.configure(bg = BG_COLOR)
        self.update_image()
