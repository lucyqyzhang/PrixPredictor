#start and login page
from tkinter import *

##startPageVisuals
def startPage(canvas, data):
    canvas.create_image(data.width//2, data.height//2, image = data.startPageImage)

def loginInfo(data, canvas):
    if data.hideUser == True and data.mode == "login":
        data.userEntry.lift()
        data.userButton.lift()
        data.hideUser = False
    else:
        data.userEntry.place(x=data.width//4 + 7, y=data.height//2-30)
        data.userButton.place(x=data.width//2.46, y=data.height//2 + 50 )
    canvas.create_image(data.width//2, data.height//2, image = data.loginPageImage)
 
    

