'''
This file:
	1. Reads in the csv file and creates a one minute dataframe
	2. The one minute dataframe is resampled to create the following:
		a. 5 minute dataframe with a 15 exponential moving average column
			and a 20 moving average column
		b. 15 minute dataframe with columns for 12 and 26 exponential moving
			averages, a column for the MACD, and a column for the difference
			in MACD.
	3. Outputs a potential call purchase when the following conditions
	are met:
		a. The 5 minute closing price is above the 20 moving average line
		b. The 15min MACD line has a positive slope

	4. Outputs a potential put purchase when the following conditions
	are met:
		a. The 5 minute closing price is below the 20 moving average line
		b. The 15min MACD line has a negative slope

'''

import numpy as np
import pandas as pd 



#1. Read in csv to dataframe and shift prices to get a fill at 9:30:
columns = ['date','close']
df = pd.read_csv('stockPrices/closingPrices-apr3.csv',names=columns,index_col='date',parse_dates=True)
df['close'] = df['close'].shift()

#2. Calculate 5minCandle 15ema,20ma & display it
df5min = df.resample('5T').last().between_time(start_time='9:30',end_time='15:55')
df5min['close'].replace('',np.nan,inplace=True)
df5min.dropna(subset=['close'], inplace=True)
df5min['20ma'] = df5min.rolling(20).mean()
df5min['15ema'] = df5min['close'].ewm(span=15,min_periods=35).mean()


#3. Calculate 15minCandle MACD difference & display it
df15min = df.resample('15T').last().between_time(start_time='9:30',end_time='15:55')
df15min['close'].replace('',np.nan,inplace=True)
df15min.dropna(subset=['close'], inplace=True)
df15min['12ema'] = df15min['close'].ewm(span=12,min_periods=28).mean()
df15min['26ema'] = df15min['close'].ewm(span=26,min_periods=58).mean()
df15min['macd'] = df15min['12ema']-df15min['26ema']
df15min['difference']=df15min['macd'].rolling(2).apply(lambda x:x[-1]-x[0],raw=True)

#4. Print out display: 

print('\n1min Data:')
print(df.index[1],"\nclose:",df.iloc[1,0])

print('\n5min Data:')
print(df5min.index[-1])

emaPosition15 = 'empty'
maPosition20 = 'emtpy'
if(df5min.iloc[-1,2]<df5min.iloc[-1,1]):
	emaPosition15 = 'bottom'
	maPosition20 = 'top'

elif(df5min.iloc[-1,2]==df5min.iloc[-1,1]):
	emaPosition15 = 'equal'
	maPosition20 = 'equal'
else: 
	emaPosition15 = 'top'
	maPosition20 = 'bottom'

print('5min15ema:',round(df5min.iloc[-1,2]*100)/100,emaPosition15)
print('5min20ma',round(df5min.iloc[-1,1]*100)/100,maPosition20)

print('\n15min MACD Data:')
print(df15min.index[-1])
print(round(df15min.iloc[-1,3]*100)/100)

