# pythonStockAnalyzer

This program downloads stock data from http://alphavantage.co and outputs a message for a potential purchase of either a call or a put. 

Contents: 
  1. download_alphaPrices.py
  This file:
   A. downloads 5 days of minute stock data in JSON format from alphavantage.co
   B. creates a dictionary with one key-value pair: {datetime:closingPrice}
   C. saves the dictionary to a csv file
   D. prints whether connection and download were successful

  Note:
  You need a free API key in order to download the data.
  Obtain API here:
  https://www.alphavantage.co/support/#api-key
  Replace your api key with the x's in the url connection variable named "url"
  
  2. main_v1.py
  This file:
	A. Reads in the csv file and creates a one minute dataframe
	B. The one minute dataframe is resampled to create the following:
		a. 5 minute dataframe with a 15 exponential moving average column
			and a 20 moving average column
		b. 15 minute dataframe with columns for 12 and 26 exponential moving
			averages, a column for the MACD, and a column for the difference
			in MACD.
	C. Outputs a potential call purchase when the following conditions
	are met:
		a. The 5 minute closing price is above the 20 moving average line
		b. The 15min MACD line has a positive slope
	D. Outputs a potential put purchase when the following conditions
	are met:
		a. The 5 minute closing price is below the 20 moving average line
		b. The 15min MACD line has a negative slope
