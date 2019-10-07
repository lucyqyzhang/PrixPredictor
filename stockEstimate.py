#asks for user input on stock price estimation
from topBottom import *
from tkinter import *

##stockEstimateVisual
def getInfo(data, canvas):
    data.wantedStock = data.entry.get()
    data.sevenDays, data.hundredDays, data.oneYr, data.twoYr = getStockResult(data)
    data.entry.delete(0, END)
    data.mode = "stockResult"

def stockEstimateVisuals(canvas, data):
    if data.hideEntry == True and data.mode == "stockEstimate":
        data.entry.lift()
        data.enter.lift()
        data.hideEntry = False
    if data.hideBuy == False and data.hideSell == False:
        data.buy.lower()
        data.sell.lower()
        data.hideBuy, data.hideSell = True, True
    else:
        data.entry.place(x = data.width//4 - 65, y = 2*data.height//3+55)
        data.enter.place(x = 3*data.width//4 - 20, y = 2*data.height//3+50)
        data.hideEntry = False
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
    canvas.create_image(data.width//2, data.height//2, image = data.stockestimateImage)
    canvas.create_text(data.width//2, data.height//2 - 100, text = data.curUser + " !", fill = data.colour, font = (data.font, 30))
    stock = StringVar()
    
##predictionMath
#https://medium.com/python-data/effient-frontier-in-python-34b0c3043314
#https://pythonprogramming.net/sp500-company-list-python-programming-for-finance/

import math
import numpy as np
import datetime 
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as pet
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from scipy.stats import norm
import matplotlib.mlab as mlab

class monteCarlo:
    def __init__(self, stock, start, end, timeLength):
        self.start = start
        self.end = end
        self.stock = stock
        self.timeLength = timeLength
    
    def getVariables(self):
        #get prices for this time period
        start = self.start 
        end = self.end 
        prices = web.DataReader(self.stock, 'yahoo',start, end)['Adj Close']
        returns = prices.pct_change()
        self.returns = returns
        self.prices = prices
    
    def calculateVariables(self):
        self.getVariables()
        #find percentage change, mean, and variance
        logReturns = np.log(1 + self.returns)
        u = logReturns.mean()
        variance = logReturns.var()
        drift = u - (0.5 * variance)
        standev = logReturns.std()
        zValue = norm.ppf(np.random.rand(10,2))
        
        self.drift = drift
        self.standev = standev
    
    def futureReturns(self):
        self.calculateVariables()
        #forecast price in the next 100 days
        self.timeInterv = self.timeLength
        self.iterations = 10
        self.drift = np.array(self.drift)
        self.standev = np.array(self.standev)
        dailyReturns = np.exp(self.drift + self.standev * norm.ppf(np.random.rand(self.timeInterv, self.iterations)))
        
        s0 = self.prices.iloc[-1]
        priceList = np.zeros_like(dailyReturns)
        priceList[0] = s0
        for i in range(1, self.timeInterv):
            priceList[i] = priceList[i-1] * dailyReturns[i]
        self.priceList = priceList
    
    def brownian_motion(self, num_simulations, predicted_days):
        returns = self.returns
        prices = self.prices

        last_price = prices[-1]

        #Note we are assuming drift here
        simulation_df = pd.DataFrame()
        
        #Create Each Simulation as a Column in df
        for x in range(num_simulations):
            
            #Inputs
            count = 0
            avgReturns = returns.mean()
            variance = returns.var()
            
            daily_vol = returns.std()
            daily_drift = avgReturns - (variance/2)
            drift = daily_drift - 0.5 * daily_vol ** 2
            
            #Append Start Value    
            prices = []
            
            shock = drift + daily_vol * np.random.normal()
            last_price * math.exp(shock)
            prices.append(last_price)
            
            for i in range(predicted_days):
                if count == 251:
                    break
                shock = drift + daily_vol * np.random.normal()
                price = prices[count] * math.exp(shock)
                prices.append(price)
                
        
                count += 1
            simulation_df[x] = prices
            self.simulation_df = simulation_df
            self.predicted_days = predicted_days
        
    def mcSim(self):
        self.futureReturns()
        new = []
        for col in range(len(self.priceList[0])):
            for row in range (len(self.priceList)):
                if row == len(self.priceList) - 1:
                    new.append(self.priceList[row][col])
        finalSum = 0
        for num in new:
            finalSum += num
        return finalSum/self.iterations
    