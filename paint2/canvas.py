from tkinter import Canvas, filedialog
from PIL import Image, ImageDraw, ImageTk
from settings import *
import random

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
        self.tag_lower(self.canvas_image)

    def clear(self):
        self.delete('all')

        self.image = Image.new('RGB',
                               (self.winfo_width(), self.winfo_height()),
                               BG_COLOR)
        self.draw = ImageDraw.Draw(self.image)

        self.configure(bg = BG_COLOR)
        self.update_image()

    def open_dialog(self):
        path = filedialog.askopenfilename()
        self.Open_Image(path)

    def Open_Image(self, path):
        # Open the image first
        self.image = Image.open(path)

        # Setting the variables needed to resize the image
        canvas_width, canvas_height = self.winfo_width(), self.winfo_height()
        self.image_ratio = self.image.size[0] / self.image.size[1]

        # Scale the image to match the canvas height first
        image_height = canvas_height
        image_width = int(image_height * self.image_ratio)

        # Resize the image
        resized_image = self.image.resize((image_width, image_height))

        # Crop if the image width exceeds the canvas width
        if image_width > canvas_width:
            left = (image_width - canvas_width) // 2 # left side of the image
            right = left + canvas_width # Right side of the image
            resized_image = resized_image.crop((left, 0, right, image_height)) # cropping the image to make it fit

        # Update self.image to the resized and potentially cropped version
        self.image = resized_image

        # Displaying the image on the canvas
        self.canvas_image = ImageTk.PhotoImage(self.image)
        self.create_image(0, 0, image=self.canvas_image, anchor='nw')

        self.draw = ImageDraw.Draw(self.image)
        self.update_image()
        
    def Export_Image(self):
        #! I Know you can export the image in any other file dimensions but that ain't my problem
        # Open a save file dialog and get the file path
        file_path = filedialog.asksaveasfilename(
            defaultextension = ".png",  # default file extension
            filetypes = [("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
            title = "Save Image As"
        )

        # Check if a file path was selected
        if file_path:
            try:
                # Save the current image to the selected file path
                self.image.save(file_path)
            except Exception as e:
                pass

    def GenerateRandomImage(self):
        # Get canvas dimensions
        width, height = self.winfo_width(), self.winfo_height()

        # Create a new PIL image with the canvas size
        self.image = Image.new('RGB', (width, height), BG_COLOR)

        # Access the pixel map directly for faster manipulation
        pixels = self.image.load()

        palette = [
        "#000000", "#333333", "#555555", "#777777", "#999999", "#BBBBBB", "#DDDDDD", "#FFFFFF", # GrayScale
        "#8B0000", "#B22222", "#FF0000", "#FF6347", "#FF7F7F", "#FFA07A", "#FFB6C1", "#FFC0CB", # Reds 
        "#8B4513", "#A52A2A", "#D2691E", "#FF8C00", "#FFA500", "#FFB347", "#FFD700", "#FFE4B5", # Oranges
        "#FFD700", "#FFFACD", "#FFFF00", "#F0E68C", "#EEE8AA", "#FAFAD2", "#FFEFD5", "#FFF8DC", # Yellows
        "#006400", "#008000", "#32CD32", "#00FF00", "#7FFF00", "#98FB98", "#ADFF2F", "#00FA9A", # Greens
        "#008B8B", "#20B2AA", "#00CED1", "#40E0D0", "#48D1CC", "#AFEEEE", "#7FFFD4", "#E0FFFF", # Cyan
        "#00008B", "#0000CD", "#0000FF", "#4169E1", "#6495ED", "#87CEEB", "#87CEFA", "#ADD8E6", # Blues
        "#4B0082", "#6A0DAD", "#800080", "#9370DB", "#8A2BE2", "#BA55D3", "#DA70D6", "#EE82EE"  # Purples
        ]
        
        
        # Assign random colors to each pixel
        for x in range(width):
            for y in range(height):
                # Choose a random color from the palette and set the pixel
                pixels[x, y] = tuple(int(palette[random.randint(0, 63)][i:i + 2], 16) for i in (1, 3, 5))

        # Update the displayed image on the canvas
        self.draw = ImageDraw.Draw(self.image)
        self.update_image()
