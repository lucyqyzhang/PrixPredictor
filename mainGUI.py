#main GUI file 
import tkinter as tk
import os
from tkinter import *
from PIL import ImageTk
from PIL import Image
import PIL.Image
import datetime

from stockEstimate import *
from startPage import *
from stockResult import *
from stockSim import *
from buy import *
from sell import *
from api import *
from leadershipBoard import *

####################################
# customize these functions
####################################
def init(data, canvas):
    data.timer = 0
    data.font = "Montserrat"
    data.colour = "SkyBlue4"
    data.margin = data.height // 20
    data.wantedStock = ""
    data.wantedSell = ""
    data.wantedBuy = ""
    data.mode = "login"
    data.start = datetime.datetime(2009, 1, 3)
    data.end = datetime.datetime.now()
    data.current = 0
    data.sevenDays = 0
    data.oneYr = 0
    data.twoYr = 0
    data.buyAmount = 0
    data.sellAmount = 0
    data.calculateBuyAmount = 0
    data.calculateSellAmount = 0
    
    #button colours
    data.finalBuyColour = "gray89"
    data.finalSellColour = "gray89"
    
    #hide buttons
    data.hideUser = False
    data.hideEntry = False
    data.hideBuy = False
    data.hideSell = False
    data.hideAllBuy = False
    data.hideAllSell = False
    
    #stock simulation use info
    user_file = open("user.csv","r")
    data.users = dict()
    for cur_line in user_file:
        vals = cur_line.split(",")
        user_name = vals[0]
        cur_list = [("revenue",vals[1])]
        for i in range(2,len(vals)):
            items = vals[i].split("_")
            print(items)
            cur_list.append((items[0],int(items[1])))
        data.users[user_name] = cur_list
    data.curUser = ""
    data.userStocks = dict()
    data.userRevenue = 10000
    data.cannotSell = False

    #background images
    baseFolder = os.path.dirname(os.path.dirname(__file__))
    
    startPageImagePath = os.path.join(baseFolder, 'Images' + os.sep + 'startpageimage.png')
    data.startPageImage = ImageTk.PhotoImage(file = startPageImagePath)
    loginPageImagePath = os.path.join(baseFolder, 'Images' + os.sep + 'loginpageimage.png')
    data.loginPageImage = ImageTk.PhotoImage(file = loginPageImagePath)
    
    stockestimatePath = os.path.join(baseFolder, 'Images' + os.sep + 'stockestimate.png')
    data.stockestimateImage = ImageTk.PhotoImage(file = stockestimatePath)
    stockresultPath = os.path.join(baseFolder, 'Images' + os.sep + 'stockresult.png')
    data.stockresultImage = ImageTk.PhotoImage(file = stockresultPath)
    
    stocksimPath = os.path.join(baseFolder, 'Images' + os.sep + 'stocksim.png')
    data.stocksimImage = ImageTk.PhotoImage(file = stocksimPath)
    
    stockbuy1Path = os.path.join(baseFolder, 'Images' + os.sep + 'buystocks1.png')
    data.stockbuy1Image = ImageTk.PhotoImage(file = stockbuy1Path)
    stockbuy2Path = os.path.join(baseFolder, 'Images' + os.sep + 'buystocks2.png')
    data.stockbuy2Image = ImageTk.PhotoImage(file = stockbuy2Path)
    
    stocksell1Path = os.path.join(baseFolder, 'Images' + os.sep + 'sellstocks1.png')
    data.stocksell1Image = ImageTk.PhotoImage(file = stocksell1Path)
    stocksell2Path = os.path.join(baseFolder, 'Images' + os.sep + 'sellstocks2.png')
    data.stocksell2Image = ImageTk.PhotoImage(file = stocksell2Path)

    leaderPath = os.path.join(baseFolder, 'Images' + os.sep + 'leadership.png')
    data.leaderImage = ImageTk.PhotoImage(file = leaderPath)
    
    #graph_image 
    data.cur_graph = ImageTk.PhotoImage(file = "helloman.png")
    
    #widgets
    data.userEntry = Entry(canvas.master, width = 28, font = data.font)
    data.userButton = Button(canvas.master, text="Enter", font = data.font, width=10, height=2, command = lambda: storeUser(data, canvas))
    
    data.entry = Entry(canvas.master, width = 30, font = data.font)
    data.enter = Button(canvas.master, text="Enter", width=10, height=2, highlightbackground="DarkOrange2", fg="white", highlightthickness=2, 
    command = lambda: getInfo(data, canvas))
    
    data.buy = Button(canvas.master, text = "Buy", width=17, height=3, highlightbackground="DarkOrange2", fg="white", highlightthickness=2,
    command = lambda: getBuyStocks(data))
    data.sell = Button(canvas.master, text = "Sell", width=17, height=3, highlightbackground="DarkOrange2", fg="white", highlightthickness=2,
    command = lambda: getSellStocks(data))
    
    data.wantedBuyEntry = Entry(canvas.master)
    data.wantedSellEntry = Entry(canvas.master)
    data.wantedBuyButton = Button(canvas.master, text = "Enter", width=10, height=2, highlightbackground="white", fg="black", 
    highlightthickness=2, command = lambda: getInfoBuy(data))
    data.wantedSellButton = Button(canvas.master, text = "Enter", width=10, height=2, highlightbackground="white", fg="black", 
    highlightthickness=2, command = lambda: getInfoSell(data))
    
    data.calculateBuyEntry = Entry(canvas.master)
    data.calculateSellEntry = Entry(canvas.master)
    data.calculateBuyButton = Button(canvas.master, text = "Enter", width=10, height=2, highlightbackground="white", fg="black", 
    highlightthickness=2, command = lambda: getCalculateBuy(data))
    data.calculateSellButton = Button(canvas.master, text = "Enter", width=10, height=2, highlightbackground="white", fg="black", 
    highlightthickness=2, command = lambda: getCalculateSell(data))
    
    data.finalBuyButton = Button(canvas.master, text = "BUY", width=17, height=3, highlightbackground="DarkOrange2", fg="white",
    highlightthickness=2, command = lambda: getFinalBuy(data))
    data.finalSellButton = Button(canvas.master, text = "SELL", width=17, height=3, highlightbackground="DarkOrange2", fg="white",
    highlightthickness=2, command = lambda: getFinalSell(data))

def storeUser(data, canvas):
    data.curUser = data.userEntry.get()
    data.userStocks = dict()
    if (data.users.get(data.curUser,0) != 0):
        list_of_obj = data.users.get(data.curUser,0)
        for i in range(len(list_of_obj)):
            item, num = list_of_obj[i]
            if (item == "revenue"):
                data.userRevenue = float(num)
            else:
                data.userStocks[item] = num
    else:
        data.users[data.curUser] = [("revenue",data.userRevenue)]
    data.mode = "stockEstimate"
    if data.hideUser == False:
        data.userEntry.lower()
        data.userButton.lower()
        data.hideUser = True
    
def getInfo(data, canvas):
    data.wantedStock = data.entry.get()
    data.mode = "stockResult"
    data.sevenDays, data.hundredDays, data.oneYr, data.twoYr = getStockResult(data)
    data.entry.delete(0, END)

def getBuyStocks(data):
    data.mode = "buyStocks"
  
def getSellStocks(data):
    data.mode = "sellStocks"

def getInfoBuy(data):
    data.wantedBuy = data.wantedBuyEntry.get()
    data.wantedBuyEntry.delete(0, END)
    data.mode = "infoBuy"
    data.hideAllBuy = True

def getInfoSell(data):
    data.wantedSell = data.wantedSellEntry.get()
    if data.wantedSell not in data.userStocks.keys():
        data.cannotSell = True
    else:
        data.mode = "infoSell"
        data.hideAllSell = True
    data.wantedSellEntry.delete(0, END)

def getCalculateBuy(data):
    data.buyAmount = int(data.calculateBuyEntry.get())
    data.calculateBuyEntry.delete(0, END)
    data.finalBuyColour = "white"
    data.mode = "calculateBuy"
    data.curPrice = security_api.get_security_intraday_prices(data.wantedBuy, start_date=data.start, end_date=data.end)
    data.curPrice = data.curPrice.intraday_prices[0].last_price
    data.hideAllBuy = True
    data.finalBuyButton.lift()
    
def getCalculateSell(data):
    data.sellAmount = int(data.calculateSellEntry.get())
    data.calculateSellEntry.delete(0, END)
    if int(data.userStocks[data.wantedSell]) < int(data.sellAmount):
        data.cannotSell = True
        data.calculateSellEntry.lower()
        data.calculateSellButton.lower()
    else:
        data.finalSellColour = "white"
        data.mode = "calculateSell"
        data.curPrice = security_api.get_security_intraday_prices(data.wantedSell, start_date=data.start, end_date=data.end)
        data.curPrice = data.curPrice.intraday_prices[0].last_price
        data.hideAllSell = True
        data.finalSellButton.lift()

def getFinalBuy(data):
    data.userRevenue -= (data.curPrice * data.calculateBuyAmount)
    data.userStocks[data.wantedBuy] = data.userStocks.get(data.wantedBuy,0) + data.calculateBuyAmount
    newObj = [("revenue",data.userRevenue)]
    for stock in data.userStocks.keys():
        newObj.append((stock,int(data.userStocks[stock])))
    data.users[data.curUser] = newObj
    user_file = open("user.csv","w")
    user_str = ""
    for user in data.users.keys():
        cur_user_stocks = data.users[user]
        r,money = cur_user_stocks[0]
        user_str += user + "," + str(money) + ","
        for i in range(1,len(cur_user_stocks)):
            stk,num = cur_user_stocks[i]
            user_str += str(stk) + "_" + str(num) + ","
        user_str = user_str[:-1]
        user_str += "\n"
    user_str = user_str[:-1]
    user_file.write(user_str)
    data.mode = "stockSim"

def getFinalSell(data):
    data.userRevenue += (data.curPrice * data.sellAmount)
    data.userStocks[data.wantedSell] -= data.sellAmount
    newObj = [("revenue",data.userRevenue)]
    for stock in data.userStocks.keys():
        newObj.append((stock,int(data.userStocks[stock])))
    data.users[data.curUser] = newObj
    user_file = open("user.csv","w")
    user_str = ""
    for user in data.users.keys():
        cur_user_stocks = data.users[user]
        r,money = cur_user_stocks[0]
        user_str += user + "," + str(money) + ","
        for i in range(1,len(cur_user_stocks)):
            stk,num = cur_user_stocks[i]
            user_str += str(stk) + "_" + str(num) + ","
        user_str = user_str[:-1]
        user_str += "\n"
    user_str = user_str[:-1]
    user_file.write(user_str)
    data.mode = "stockSim"

def mousePressed(event, data):
    seg = data.height//10
    if 0 < event.x <= data.width//3 and data.height - seg < event.y < data.height:
        data.mode = "stockEstimate"
    elif data.width//3 < event.x <= 2*data.width//3 and data.height - seg < event.y < data.height:
        data.mode = "stockSim"
    elif 2*data.width//3 < event.x <= data.width and data.height - seg < event.y < data.height:
        data.mode = "leadershipBoard"
    data.cannotSell = False
 
def keyPressed(event, data):
    pass
    
def timerFired(data):
    data.timer += 1

def redrawAll(canvas, data):
    if data.timer < 15:
        startPage(canvas, data)
    elif data.timer >= 15:
        if data.mode == "login":
            loginInfo(data, canvas)
        elif data.mode == "stockEstimate": 
            stockEstimateVisuals(canvas, data)
        elif data.mode == "stockResult": 
            stockResultVisuals(canvas, data)
        elif data.mode == "stockSim":
            stockSimVisuals(data, canvas)
        elif data.mode == "buyStocks" or data.mode == "infoBuy" or data.mode == "calculateBuy":
            buyStocksVisuals(data, canvas)
        elif data.mode == "sellStocks" or data.mode == "infoSell" or data.mode == "calculateSell":
            sellStocksVisuals(data, canvas)
        elif data.mode == "leadershipBoard":
            leadershipBoardVisuals(data, canvas)

            
####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    init(data, canvas)
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 776)