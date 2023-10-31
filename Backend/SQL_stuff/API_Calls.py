URL	TEST		NEEDS	NEEDS	NEEDS	NEEDS
https://www.marketaux.com/documentation	Sentiment analysis		Ticker			
			
https://www.alphavantage.co/query?function=CCI&symbol=IBM&interval=daily&time_period=10&apikey=demo	CCI		Ticker	Interval(60min, daily, weekly, monthly)	Time period(+int)	
https://www.alphavantage.co/query?function=SMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo	SMA		Ticker	Interval(60min, daily, weekly, monthly)	Time period(+int)	Series Type(close, open, high, low)
https://www.alphavantage.co/query?function=EMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo	EMA		Ticker	Interval(60min, daily, weekly, monthly)	Time period(+int)	Series Type(close, open, high, low)
https://www.alphavantage.co/query?function=WMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo	WMA		Ticker	Interval(60min, daily, weekly, monthly)	Time period(+int)	Series Type(close, open, high, low)
https://www.alphavantage.co/query?function=DEMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo	DEMA		Ticker	Interval(60min, daily, weekly, monthly)	Time period(+int)	Series Type(close, open, high, low)
https://www.alphavantage.co/query?function=TEMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo	TEMA		Ticker	Interval(60min, daily, weekly, monthly)	Time period(+int)	Series Type(close, open, high, low)
https://www.alphavantage.co/query?function=MOM&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo	MOM		Ticker	Interval(60min, daily, weekly, monthly)	Time period(+int)	Series Type(close, open, high, low)
https://www.alphavantage.co/query?function=OBV&symbol=IBM&interval=weekly&apikey=demo	OBV		Ticker	Interval(60min, daily, weekly, monthly)		
https://www.alphavantage.co/query?function=STOCH&symbol=IBM&interval=daily&apikey=demo	STOCH		Ticker	Interval(60min, daily, weekly, monthly)		
https://www.alphavantage.co/query?function=MACDEXT&symbol=IBM&interval=daily&series_type=open&apikey=demo	MACDEXT		Ticker	Interval(60min, daily, weekly, monthly)	Time period(+int)	
https://www.alphavantage.co/query?function=RSI&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo	RSI		Ticker	Interval(60min, daily, weekly, monthly)	Time period(+int)	Series Type(close, open, high, low)
						
https://api.polygon.io/v1/indicators/macd/AAPL?timespan=day&adjusted=true&short_window=12&long_window=26&signal_window=9&series_type=close&order=desc&apiKey=*	MACD		Ticker	Timespan(day, week, month, year)		
https://finance.yahoo.com/quote/NVDA?p=NVDA	Anything on yahoo 		Ticker			









#############################
#Web Scraping for environmental data 
#############################

import requests
import re
	
	
def esgAPI(ticker):
	my_dict = {}
	
	# Define the URL of the webpage you want to download
	url = f'https://finance.yahoo.com/quote/{ticker}/sustainability'  # Replace with the URL of the webpage you want to download
	
	# Set the User-Agent header to mimic Mozilla Firefox
	headers = {'User-Agent': 'Mozilla/5.0'}
	
	try:
		# Send an HTTP GET request to the URL with the specified User-Agent
		response = requests.get(url, headers=headers)
		
		# Check if the request was successful (status code 200)
		if response.status_code == 200:
			# Get the HTML content of the page
			html_content = response.text
			
			# Define the target string
			target_string = '<div class="D(ib) Fz(23px) smartphone_Fz(22px) Fw(600)">'
			
			level = 0
			# Use regular expression to find and print the content between the target string and the next '<' for the first 3 instances
			for match in re.finditer(re.escape(target_string), html_content):
				start_index = match.end()
				end_index = html_content.find('<', start_index)
				
				if end_index != -1:
					content_between = html_content[start_index:end_index]
					if(level == 0):
						my_dict["Environment Risk Score"] = content_between
					elif(level == 1):
						my_dict["Social Risk Score"] = content_between
					else:
						my_dict["Governance Risk Score"] = content_between
					level += 1
			#print(f"	Instance {match.start() // len(target_string) + 1}: {content_between}")
				else:
					print(f"Instance {match.start() // len(target_string) + 1}: Content not found after target string.")
			# Stop after the first 3 instances
				if (match.start() // len(target_string) == 2):
					break
			target_string = '<div class="Fz(36px) Fw(600) D(ib) Mend(5px)">'
			for match in re.finditer(re.escape(target_string), html_content):
				start_index = match.end()
				end_index = html_content.find('<', start_index)
				if end_index != -1:
					content_between = html_content[start_index:end_index]
					my_dict["Total ESG Risk score"] = content_between
					#print(f"	Instance {match.start() // len(target_string) + 1}: {content_between}")
				else:
					print(f"Instance {match.start() // len(target_string) + 1}: Content not found after target string.")
		else:
			print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
	except requests.exceptions.RequestException as e:
		print(f"An error occurred: {str(e)}")
	return my_dict
