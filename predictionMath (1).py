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
    def __init__(self, stock, start, end):
        self.start = start
        self.end = end
        self.stock = stock
    
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
        self.timeInterv = 100
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
    
    def line_graph(self):
        prices = self.prices
        self.predicted_days = self.predicted_days
        simulation_df = self.simulation_df
        
        last_price = prices[-1]
        fig = plt.figure()
        style.use('bmh')
        
        title = "Monte Carlo Simulation: " + str(self.predicted_days) + " Days"
        plt.plot(simulation_df)
        fig.suptitle(title,fontsize=18, fontweight='bold')
        plt.xlabel('Day')
        plt.ylabel('Price ($USD)')
        plt.grid(True,color='grey')
        plt.axhline(y=last_price, color='r', linestyle='-')
        plt.show()
        
a = monteCarlo("AAPL", datetime.datetime(2009, 1, 3), datetime.datetime.now())
print(a.mcSim())
a.line_graph()
        
    