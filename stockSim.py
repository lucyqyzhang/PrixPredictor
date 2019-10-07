#stock simulation game where user revenue, user stocks, and username is stored into csv files and can be accessed when running progrm again
#using csv files because google login feature has been diabled from March 7th, 2019
#stock prices are in real time and based on real time stock price api

from topBottom import *

##stockSimVisuals
def stockSimVisuals(data, canvas):
    if data.hideEntry == False:
        data.entry.lower()
        data.enter.lower()
        data.hideEntry = True
    if data.hideBuy == True and data.hideSell == True:
        data.buy.lift()
        data.sell.lift()
        data.hideBuy, data.hideSell = False, False
    else:
        data.buy.place(x = data.width//6-30, y = 3*data.height//4 + 40)
        data.sell.place(x = 2*data.width//3 - 40, y = 3*data.height//4 + 40)
    if data.hideAllBuy == False:
        data.wantedBuyEntry.lower()
        data.wantedBuyButton.lower()
        data.calculateBuyEntry.lower()
        data.calculateBuyButton.lower()
        data.finalBuyButton.lower()
        data.hideAllBuy = True
    if data.hideAllSell == False:
        data.wantedSellEntry.lower()
        data.wantedSellButton.lower()
        data.calculateSellEntry.lower()
        data.calculateSellButton.lower()
        data.finalSellButton.lower()
        data.hideAllSell = True
        
    for key in data.users:
        if key == data.curUser:
            userRev = data.users[key][-1]
            userStock = data.users[key][0]
    
    canvas.create_image(data.width//2, data.height//2, image = data.stocksimImage)
    space = data.height-(data.height//11)-10 - (data.height//13 + 10) 
    margin = 10
    text1 = (((data.height//13+space//2-40) - (data.height//13+20))//2) + (data.height//13+20)
    canvas.create_text(data.width//2, text1 + 2*margin, text = "%s's balance:\n         $%d" %(data.curUser, data.userRevenue), fill = data.colour, font = (data.font, 30))
    canvas.create_text(data.width//2 + 10, data.height//2 + 20, text = "%s's stocks:\n" %data.curUser, fill = data.colour, font = (data.font, 30))
    
    nextLine = 20
    for key in data.userStocks.keys():
        canvas.create_text(data.width//2, data.height//2+nextLine + 20, 
        text = ("You have " + str(int(data.userStocks[key])) + " stocks of " + str(key)), 
        fill = data.colour, font = (data.font, 20))
        nextLine += 30
    
    