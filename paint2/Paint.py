import customtkinter as ctk
from canvas import canvas
from settings import *
from menu import *

class PaintApp(ctk.CTk):
    def __init__(self):
        # window setup
        super().__init__()
        self.geometry('1100x700');
        self.title('Simple Paint App')
        self.resizable(False, False)
        # self.minsize(1000, 700)
        self.columnconfigure(0, weight = 3, uniform = 'a')
        self.columnconfigure(1, weight = 7, uniform = 'a')
        self.rowconfigure(0, weight = 1)
        ctk.set_appearance_mode('dark')

        # widgets
        self.canvas = canvas(self, CURRENT_COLOR, CURRENT_TOOL, CURRENT_SLIDER_VAL)
        self.menu = Menu(self, self.canvas)

        # run
        self.update_idletasks()
        self.mainloop()

if __name__ == '__main__':
    PaintApp()
