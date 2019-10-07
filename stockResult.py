#gives stock price estimation result based on user input
#creates real time graph of the stock, and price will adjust every 5 minutes
from stockEstimate import *
from topBottom import *
from api import *
from PIL import ImageTk
from PIL import Image

##stockResultCalculation
def getStockResult(data):
    seven = monteCarlo(data.wantedStock, data.start, data.end, 7)
    hundred = monteCarlo(data.wantedStock, data.start, data.end, 100)
    oneYr = monteCarlo(data.wantedStock, data.start, data.end, 252)
    twoYr = monteCarlo(data.wantedStock, data.start, data.end, 504)
    data.sevenDays = seven.mcSim()
    data.hundredDays = hundred.mcSim()
    data.oneYr = oneYr.mcSim()
    data.twoYr = twoYr.mcSim()
    return data.sevenDays, data.hundredDays, data.oneYr, data.twoYr

##stockResultVisual
def stockResultVisuals(canvas, data):
    if data.hideEntry == False:
        data.entry.lower()
        data.enter.lower()
        data.hideEntry = True
        
    canvas.create_image(data.width//2, data.height//2, image = data.stockresultImage)
    space = data.height-(data.height//11)-10 - (data.height//13 + 10) 
    margin = 10
    graphEnd = data.height//13+20+space//2.5
    bottom = data.height-(data.height//11)-10
    canvas.create_text((margin+data.width//2)//2, (bottom-graphEnd)//4 + graphEnd + 60, text = "7 DAY FORECAST\n            $%d" %data.sevenDays,  
    fill = data.colour, font = (data.font, 22))
    canvas.create_text((data.width//2+data.width-margin)//2, (bottom-graphEnd)//4 + graphEnd + 60, 
    text = "100 DAY FORECAST\n             $%d" %data.hundredDays, fill = data.colour, font = (data.font, 22))
    canvas.create_text((margin+data.width//2)//2, 3*(bottom-graphEnd)//4 + graphEnd, 
    text = "1 YEAR FORECAST\n            $%d" %data.oneYr, fill = data.colour, font = (data.font, 22))
    canvas.create_text((data.width//2+data.width-margin)//2, 3*(bottom-graphEnd)//4 + graphEnd, 
    text = "2 YEAR FORECAST\n            $%d" %data.twoYr, fill = data.colour, font = (data.font, 22))
    
    #get real time stock price using api
    api_response = security_api.get_security_intraday_prices(data.wantedStock, start_date = data.start, end_date = data.end)
    stock_data = api_response.intraday_prices
    prices = []
    for i in range (len(stock_data)):
        prices.append(stock_data[i].last_price)
    
    num_prices = len(prices)
    x = np.linspace(num_prices-1,0, num_prices)
    plt.xlabel("Days Ago")
    plt.ylabel("Market Price (per share)")
    plt.plot(x, prices, "r", linewidth = 3.0, label = "%s's 'Market Trend" %data.wantedStock)
    plt.savefig('helloman.png')
    file_in = 'helloman.png'
    pil_image = Image.open(file_in)
    graph = pil_image.resize((500, 220), Image.ANTIALIAS)
    file_out = 'helloman.png'
    graph.save(file_out)
    #data.cur_graph = ImageTk.PhotoImage(file = "helloman.png")
    canvas.create_image(data.width//2, data.height//3, image=data.cur_graph)
    #plt.show()
