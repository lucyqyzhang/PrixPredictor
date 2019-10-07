#page for selling stocks based on user input, removes stocks for users and adds revenue to user revenue
#stock prices are in real time and based on real time stock price api
from topBottom import *
from api import *

def sellStocks(data):
    data.userRevenue = data.userRevenue - (curPrice*data.calculateSellAmount)
    data.userStocks.remove(data.wantedStock)
    data.mode = "stockSim"
    
def sellStocksVisuals(data, canvas):
    canvas.create_image(data.width//2, data.height//2, image = data.stocksell1Image)
    if data.hideBuy == False and data.hideSell == False:
        data.buy.lower()
        data.sell.lower()
        data.hideBuy, data.hideSell = True, True
    if data.hideAllSell == True:
        data.wantedSellEntry.lift()
        data.wantedSellButton.lift()
        if data.cannotSell == True:
            canvas.create_text(data.width//2, 2*data.height//3, text = "You cannot sell this stock!", fill = data.colour, font = (data.font, 30))
            data.calculateSellEntry.lower()
            data.calculateSellButton.lower()
            canvas.create_image(data.width//2, data.height//2, image = data.stocksell1Image)
        elif data.mode == "infoSell":
            data.calculateSellEntry.lift()
            data.calculateSellButton.lift()
        elif data.mode == "calculateSell":
            data.finalSellButton.lift()
        data.hideAllSell = False
    else:
        data.wantedSellEntry.place(x = data.width//3, y =data.height//3 - 25)
        data.wantedSellButton.place(x = data.width//2.4, y =data.height//3 + 15)
        if data.cannotSell == True:
            canvas.create_text(data.width//2, 2*data.height//3, text = "You cannot sell this stock!", fill = data.colour, font = (data.font, 30))
            data.calculateSellEntry.lower()
            data.calculateSellButton.lower()       
        elif data.mode == "infoSell":
            data.calculateSellEntry.place(x = data.width//3, y = 2*data.height//3 - 70)
            data.calculateSellButton.place(x = data.width//2.4, y = 2*data.height//3 - 25)
            canvas.create_image(data.width//2, data.height//2, image = data.stocksell2Image)
        elif data.mode == "calculateSell":
            data.finalSellButton.place(x = data.width//2.7, y = 3*data.height//4  + 40)
        data.hideAllSell = False

    if data.mode == "calculateSell":
        if data.cannotSell == True:
            canvas.create_text(data.width//2, 2*data.height//3, text = "You cannot sell this stock!", fill = data.colour, font = (data.font, 30))
            data.calculateSellEntry.lower()
            data.calculateSellButton.lower()        
        else:
            data.calculateSellAmount = (int(data.sellAmount))*data.curPrice
            canvas.create_image(data.width//2, data.height//2, image = data.stocksell2Image)
            canvas.create_text(data.width//2, 3*data.height//4 + 10, 
            text = "You can sell %d stocks of %s for $%0.2f" %(data.sellAmount, data.wantedSell,data.calculateSellAmount), 
            fill = data.colour, font = (data.font, 20))
    