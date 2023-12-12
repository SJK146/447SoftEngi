#Kyle
import requests
import json

alphaAPIKey = "SAF9JC6ZQOYQAVQV"

#replace print with this to save information
def record(data):
    with open("historicCalls.txt", "a") as file:
        file.write(data)
        file.write("\n")

#sma https://www.alphavantage.co/query?function=SMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo
def alpha_SMA(symbol, interval, time_period, series_type):
    function = "SMA"
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={alphaAPIKey}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        #print(data)
        most_recent_sma_entry = next(iter(data["Technical Analysis: SMA"].values()))
        first_value = float(most_recent_sma_entry["SMA"])
        #print(first_value)
        return first_value

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

#ema https://www.alphavantage.co/query?function=EMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo
def alpha_EMA(symbol, interval, time_period, series_type):
    function = "EMA"
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={alphaAPIKey}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        #print(data)
        first_date = next(iter(data[f'Technical Analysis: {function}']))
        first_value = data[f'Technical Analysis: {function}'][first_date][function]
        #print(first_value)
        return first_value
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

#madcext https://www.alphavantage.co/query?function=MACDEXT&symbol=IBM&interval=daily&series_type=open&apikey=demo
def alpha_macdcext(symbol, interval, series_type):
    function = "MACDEXT"
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&series_type={series_type}&apikey={alphaAPIKey}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        #print(data)
        first_entry_macdext = next(iter(data["Technical Analysis: MACDEXT"].values()))
        macd_value = float(first_entry_macdext["MACD"])
        #print(macd_value)
        return macd_value

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

#rsi https://www.alphavantage.co/query?function=RSI&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo
def alpha_rsi(symbol, interval, time_period, series_type):
    function = "RSI"
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={alphaAPIKey}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        #print(data)
        first_date = next(iter(data[f'Technical Analysis: {function}']))
        first_value = data[f'Technical Analysis: {function}'][first_date][function]
        return first_value
        #print(first_value)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

#BBANDS https://www.alphavantage.co/query?function=BBANDS&symbol=IBM&interval=weekly&time_period=5&series_type=close&apikey=FV940XIF9BKNU8P5
def alpha_bands(symbol, interval, time_period, series_type):
    function = "BBANDS"
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={alphaAPIKey}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        #print(data)
        first_entry = next(iter(data["Technical Analysis: BBANDS"].values()))
        real_middle_band = float(first_entry["Real Middle Band"])
        #print(real_middle_band)
        return real_middle_band
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    
#STOCH https://www.alphavantage.co/query?function=STOCH&symbol=IBM&interval=daily&apikey=demo
def alpha_stoch(symbol, interval):
    function = "STOCH"
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&apikey={alphaAPIKey}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        #print(data)
        first_entry_stoch = next(iter(data["Technical Analysis: STOCH"].values()))
        # Extract the value of the "SlowD"
        first_entry_stoch = next(iter(data["Technical Analysis: STOCH"].values()))
        slowd_value = float(first_entry_stoch["SlowD"])
        #print(slowd_value)
        return slowd_value
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

#Polygon.io key
polyAPIkey = "4JtLI7Qc6imRdHeu4zmxImRud6hQswbQ"

#macd https://api.polygon.io/v1/indicators/macd/AAPL?timespan=day&adjusted=true&short_window=12&long_window=26&signal_window=9&series_type=close&order=desc&apiKey=*
def poly_macd(symbol, timespan):
    function = "macd"
    url = f"https://api.polygon.io/v1/indicators/macd/{symbol}?timespan={timespan}&adjusted=true&short_window=12&long_window=26&signal_window=9&series_type=close&order=desc&apiKey={polyAPIkey}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        #print(data)
        first_date = next(iter(data[f'Technical Analysis: {function}']))
        first_value = data[f'Technical Analysis: {function}'][first_date][function]
        #print(first_value)
        return first_value

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")





#validated
#alpha_EMA("TSLA", "weekly", "10", "close")
#print()
#alpha_macdcext("TSLA", "daily", "open")
#print()
#validated
#alpha_rsi("TSLA", "weekly", "10", "close")
#print()
#alpha_SMA("TSLA", "weekly", "10", "close")
#print()
#poly_macd("TSLA", "day")
#alpha_bands("TSLA", "weekly", "10", "close")
#print()
#alpha_stoch("TSLA", "weekly")
#print()


#############################
#Web Scraping for environmental data 
#############################
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
