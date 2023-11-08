https://docs.google.com/spreadsheets/d/1glnLrH92hvDENHy2s_REYXJ2cGgpRx10YTlDqKx7xmU/edit?usp=sharing



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
