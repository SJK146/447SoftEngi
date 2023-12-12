#TODO in main 

import os
import sys
import API_Calls

from flask import Flask
#from data_processor import run_data_processor
# from api_handler import handle_api_requests
from flask_sqlalchemy import SQLAlchemy
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import Study, StudyTest

#email stuff 
import smtplib
import ssl
from email.message import EmailMessage

#Timer waiting 
import datetime 
import time


#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'db.sqlite'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SECRET_KEY'] = 'the_secret_key'

#db.init_app(app)



#python interface loqgkkmgewvxefoj
def send_email(recipient_email):
    password = "WAAAAAAAAAABALLS"
    sender = "softengprojemail@gmail.com"
    subject = "Stock Trigger Notification"
    body = "Hello, your stock has hit its trigger!"

    em = EmailMessage()
    em["From"] = "softengprojemail@gmail.com"
    em["To"] = recipient_email
    em["Subject"] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, recipient_email, em.as_string())

def run_data_processor(session):
    #studies = Study.query.all()
    studies = session.query(StudyTest).all()
    #db.session.query(Study).all()

    study_data = []
    for item in studies:
        study_data.append({
            "id": item.id,
            "name": item.name,
            "study_id": item.study_id,
            "test_id": item.test_id,
            "input_1": item.input_1,
            "input_2": item.input_2,
            "input_3": item.input_3,
            "input_4": item.input_4,
            #"user_id": item.user_id,
            #"ticker": item.ticker,
            #"studies": item.studies,
        })

    return study_data

import re
import requests

if __name__ == '__main__':

    response = requests.get("http://127.0.0.1:5000/get_studies")
    if response.status_code == 200:
        # Parse the JSON data into a Python list
        data = response.text
        # Find all matches using the pattern
        matches = re.findall(r'(\S+) (\S+), \{(.+?)\}', data)

        for match in matches:
            print(match)
            email = match[0]
            ticker = match[1]
            argue = match[2].split()
            compstr = argue[2]
            value = argue[0]
            time_period = -1
            series_type = "close"

            interval = "monthly"
            if(argue[1].find("d")):
                interval = "daily"
            elif (argue[1].find("w")):
                interval = "weekly"
            returnVale = -1

            if(len(argue) == 5):#set time_period
                temp = re.search(r'\((\d+)\)', argue[4])
                time_period = int(temp.group(1))
            else:
                time_period = -1

            try:
                if value.find('SMA') != -1:
                    returnVale = API_Calls.alpha_SMA(ticker, interval, time_period, series_type)
                elif value.find('EMA') != -1:
                    returnVale = API_Calls.alpha_EMA(ticker, interval, time_period, series_type)
                elif value.find('RSI') != -1:
                    returnVale = API_Calls.alpha_rsi(ticker, interval, time_period, series_type)
                elif value.find('MACDEXT') != -1:
                    returnVale = API_Calls.alpha_macdcext(ticker, interval, series_type)
                elif value.find('BBANDS') != -1:
                    returnVale = API_Calls.alpha_bands(ticker, interval, time_period, series_type)
                elif value.find('STOCH') != -1:
                    returnVale = API_Calls.alpha_stoch(ticker, interval)
                elif value.find('MACD') != -1:
                    returnVale = API_Calls.alpha_macdcext(ticker, interval, series_type)
                #print(returnVale)
                # make comparison
                match = re.search(r'ComparisonBeingMade\((&gt;|&lt;)\)', compstr)
                valMatch = re.search(r'\((\d+)\)', argue[3])
                compValue = int(valMatch.group(1))
                if match.group(1) == '&gt;':#greater than
                    if compValue < returnVale:
                        print(f"sending email{email}")
                        send_email(email)
                else:
                    if compValue < returnVale:
                        print(f"sending email{email}")
                        send_email(email)
            except:
                print("failed on user ticker")

    # Create a database engine
    exit()
    engine = create_engine('sqlite:///../instance/db.sqlite')  # Adjust the URI based on your actual database location
    
    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()
    test = run_data_processor(session)
    print(test)
    for element in test:
        print(element)

    # handle_api_requests()


#SMA, EMA, RSI, MACDEXT, BBANDS, STOCH, MACD
#list of comparisons, compare return value to db value 
#API_Calls.alpha_SMA(symbol, interval, time_period, series_type)
#API_Calls.alpha_EMA(symbol, interval, time_period, series_type)
#API_Calls.alpha_macdcext(symbol, interval, series_type)
#API_Calls.alpha_rsi(symbol, interval, time_period, series_type)
#API_Calls.alpha_bands(symbol, interval, time_period, series_type)
#API_Calls.alpha_stoch(symbol, interval)
#API_Calls.poly_macd(symbol, timespan)


