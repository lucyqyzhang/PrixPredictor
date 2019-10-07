#creates leadership board of top three users based on their revenue
import operator
from topBottom import *

def leadershipBoardVisuals(data, canvas):
    if data.hideEntry == False:
        data.entry.lower()
        data.enter.lower()
        data.hideEntry = True
    if data.hideBuy == False and data.hideSell == False:
        data.buy.lower()
        data.sell.lower()
        data.hideBuy, data.hideSell = True, True
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
        
    canvas.create_image(data.width//2, data.height//2, image =  data.leaderImage)
    user_file = open("user.csv","r")
    all_user = []
    for cur_line in user_file:
        vals = cur_line.split(",")
        user_name = vals[0]
        user_rev = vals[1]
        all_user.append((user_name, user_rev))
    all_user.sort(key = operator.itemgetter(1), reverse = True)
    space = 105
    for i in range (len(all_user)):
        canvas.create_text(data.width//2, data.height//2.56 + space*i, 
        fill = data.colour, font = (data.font, 30), text = all_user[i][0] + "\n$" + all_user[i][1])
        
        