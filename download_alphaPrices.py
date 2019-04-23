'''
This file:
 1. downloads 5 days of minute stock data in JSON format from alphavantage.co
 2. creates a dictionary with one key-value pair: {datetime:closingPrice}
 3. saves the dictionary to a csv file
 4. prints whether connection and download were successful

Note:
You need a free API key in order to download the data.
Obtain API here:
https://www.alphavantage.co/support/#api-key

Replace your api key with the x's in the url variable below.
'''

import csv
from datetime import datetime
from pytz import timezone
import requests


# extract and save data from Alpha API
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&outputsize=full&interval=1min&symbol=SPY&apikey=xxxxxxxxxxxxxxxx&datatype=json'
r = requests.get(url)
if r.status_code == 200:
	print('Connected to Alpha API')
response_file = r.json()
	
# create blank dictionary
date = 0
closePrice = 0
dict_data = {}

# fill dictionary with select info from alphaAPI json data:
for each in response_file['Time Series (1min)'].keys():
    date = each
    closePrice = response_file['Time Series (1min)'][each]['4. close']
    dict_data.update({date:closePrice})

# create file name:
currentDate = datetime.now(timezone('US/Eastern')).strftime('%b%d').lower()
filename = 'stockPrices/closingPrices-' + currentDate + '.csv'

# write dict_data to csv
w=csv.writer(open(filename,"w",newline=''))
for key,val in dict_data.items():
	w.writerow([key,val])

now = datetime.now(timezone('US/Eastern')).strftime('%H:%M:%S %Z')
print('Current data saved at', now)
print(filename)





