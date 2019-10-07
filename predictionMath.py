import math
import numpy as np
import datetime 
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from scipy.stats import norm
from matplotlib import style
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
        
        title = "Monte Carlo Simulation: " + str(predicted_days) + " Days"
        plt.plot(simulation_df)
        fig.suptitle(title,fontsize=18, fontweight='bold')
        plt.xlabel('Day')
        plt.ylabel('Price ($USD)')
        plt.grid(True,color='grey')
        plt.axhline(y=last_price, color='r', linestyle='-')
        plt.show()
    
'''def key_stats(self):
        simulation_df = self.simulation_df

        print ('#------------------Simulation Stats------------------#')
        count = 1
        for column in simulation_df:
            print ("Simulation", count, "Mean Price: ", 
                    simulation_df[column].mean())
            print ("Simulation", count, "Median Price: ", 
                    simulation_df[column].median())
            count += 1
        
        print '\n'
        print '#----------------------Last Price Stats--------------------#'
        print "Mean Price: ", np.mean(simulation_df.iloc[-1,:])
        print "Maximum Price: ",np.max(simulation_df.iloc[-1,:])
        print "Minimum Price: ", np.min(simulation_df.iloc[-1,:])
        print "Standard Deviation: ",np.std(simulation_df.iloc[-1,:])

        print '\n'
       
        print '#----------------------Descriptive Stats-------------------#'
        price_array = simulation_df.iloc[-1, :]
        print price_array.describe()

        print '\n'
               
        print '#--------------Annual Expected Returns for Trials-----------#'
        count = 1
        future_returns = simulation_df.pct_change()
        for column in future_returns:
            print "Simulation", count, "Annual Expected Return", 
            "{0:.2f}%".format((future_returns[column].mean() * 252) * 100)
            print "Simulation", count, "Total Return", 
            "{0:.2f}%".format((future_returns[column].iloc[1] / 
            future_returns[column].iloc[-1] - 1) * 100)
            count += 1   
        print '\n'
                         
        #Create Column For Average Daily Price Across All Trials
        simulation_df['Average'] = simulation_df.mean(axis=1)
        ser = simulation_df['Average']
        
        print '#----------------------Percentiles----------------------------#'
        percentile_list = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 
                            65, 70, 75, 80, 85, 90, 95]
        for per in percentile_list:
            print "{}th Percentile: ".format(per), np.percentile(price_array, per)
        print '\n'
        print '#-----------------Calculate Probabilities----------------------#'
        print "Probability price is between 30 and 40: ",  
        "{0:.2f}%".format((float(len(price_array[(price_array&gt; 30) &amp; 
        (price_array&lt;- 40)])) / float(len(price_array)) * 100)) 
        print "Probability price is &gt; 45: ", 
        "{0:.2f}%".format((float(len(price_array[price_array &gt; 45])) / 
        float(len(price_array)))* 100)'''
        
start = datetime.datetime(2009, 1, 3)
end = datetime.datetime.now()

sim = monteCarlo("TSLA", start, end)
print(sim.mcSim())
    