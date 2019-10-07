from tkinter import *

##header & footer visuals
def header(canvas, data):
    canvas.create_image(data.width//2, data.height//2, image = data.templateImage)

