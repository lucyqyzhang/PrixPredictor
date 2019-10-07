#page for buying stocks based on user input, calculates stocks for users and deducts from user revenue
#stock prices are in real time and based on real time stock price api
from topBottom import *
from api import *

def buyStocks(data):
    data.userRevenue = data.userRevenue - (curPrice*data.calculateBuyAmount)
    data.userStocks.append(data.wantedStock)
    data.mode = "stockSim"
    
def buyStocksVisuals(data, canvas):
    canvas.create_image(data.width//2, data.height//2, image = data.stockbuy1Image)
    if data.hideBuy == False and data.hideSell == False:
        data.buy.lower()
        data.sell.lower()
        data.hideBuy, data.hideSell = True, True
    if data.hideAllBuy == True:
        data.wantedBuyEntry.lift()
        data.wantedBuyButton.lift()
        if data.mode == "infoBuy":
            data.calculateBuyEntry.lift()
            data.calculateBuyButton.lift()
        elif data.mode == "calculateBuy":
            data.finalBuyButton.lift()
        data.hideAllBuy = False
    else:
        data.wantedBuyEntry.place(x = data.width//3, y =data.height//3 - 25)
        data.wantedBuyButton.place(x = data.width//2.4, y =data.height//3 + 15)
        if data.mode == "infoBuy":
            data.calculateBuyEntry.place(x = data.width//3, y = 2*data.height//3 - 70)
            data.calculateBuyButton.place(x = data.width//2.4, y = 2*data.height//3 - 25)
            canvas.create_image(data.width//2, data.height//2, image = data.stockbuy2Image)
        elif data.mode == "calculateBuy":
            data.finalBuyButton.place(x = data.width//2.7, y = 3*data.height//4  + 40)
        data.hideAllBuy = False
    
    if data.mode == "calculateBuy":
        data.calculateBuyAmount = (int(data.buyAmount))//data.curPrice
        canvas.create_image(data.width//2, data.height//2, image = data.stockbuy2Image)
        canvas.create_text(data.width//2, 3*data.height//4 + 10, text = "You can buy %d stocks from %s" %(data.calculateBuyAmount, data.wantedBuy), 
        fill = data.colour, font = (data.font, 20))
    