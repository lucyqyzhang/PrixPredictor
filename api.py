from __future__ import print_function
import time
import intrinio_sdk
from intrinio_sdk.rest import ApiException
import datetime
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np

#use api from intrinio (https://intrinio.com)
intrinio_sdk.ApiClient().configuration.api_key['api_key'] = 'OmIxNGE4Mzg0MTA2OTQ3M2NkOTQxNzE2ZTA0MDQ4YmU5'
security_api = intrinio_sdk.SecurityApi()

# identifier = 'AAPL' # str | A Security identifier (Ticker, FIGI, ISIN, CUSIP, Intrinio ID)
# start_date = '2019-01-03' # date | Return intraday prices starting at the specified date (optional)
# end_date = datetime.datetime.now() # date | Return intraday prices stopping at the specified date (optional)


# try:
#     api_response = security_api.get_security_intraday_prices(identifier, start_date=start_date, end_date=end_date)
#     #print(api_response.intraday_prices[0].last_price)
# except ApiException as e:
#     print("Exception when calling SecurityApi->get_security_intraday_prices: %s\n" % e)
# 
# data = api_response.intraday_prices
# prices = []
# for i in range (len(data)):
#     prices.append(data[i].last_price)
# 
# num_prices = len(prices)
# x = np.linspace(0, num_prices-1,num_prices)
# plt.xlabel("Time")
# plt.ylabel("Market Price (per share)")
# plt.plot(x, prices, "r", linewidth = 3.0, label = "Market Trend")
# plt.show()

'''class info(api):
    def __init__(self, symbol):
        super.__init__(symbol)
    
    def getInfo(self):
        company_api = intrinio_sdk.CompanyApi()
        #company identifier
        identifier = self.symbol 
    
        try:
            api_response = company_api.get_company(identifier)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CompanyApi->get_company: %s\n" % e)
            
stock_exchange_api = intrinio_sdk.StockExchangeApi()

identifier = 'USCOMP' # str | A Stock Exchange identifier (MIC or Intrinio ID)
source = '' # str | Return realtime prices from the specified data source (optional)
page_size = 10 # float | The number of results to return (optional) (default to 100)
next_page = '' # str | Gets the next page of data from a previous API call (optional)

try:
    api_response = stock_exchange_api.get_stock_exchange_realtime_prices(identifier, source=source, page_size=page_size, next_page=next_page)
    print(api_response)
   
except ApiException as e:
    print("Exception when calling StockExchangeApi->get_stock_exchange_realtime_prices: %s\n" % e)

value = "AAPL"
d = api_response

def findStockPrice(d, value):
    if isinstance(d, str) and not (d == value):
        #base case
        #checks if path has gone to the end and ends path value if d != value
        return None
    elif isinstance(d, str) and (d == value):
        #checks if path has gone to the end and return [] when value is found
        return 0
    else:
        #recursive case
        for key in d:
            if key == 'stock prices':
                newDict = d[key]
                #find the path of the next path
                ifPath = findCategoryPath(newDict, value)
                #check if path is not dead
                if not ifPath == None:
                    if key == 'last_price':
                        return newDict[key]
    #if no path had value, return None
    return None'''

