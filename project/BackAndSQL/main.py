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
            "input_1": item.input_2,
            "input_1": item.input_3,
            "input_1": item.input_4,
            #"user_id": item.user_id,
            #"ticker": item.ticker,
            #"studies": item.studies,
        })

    return study_data


if __name__ == '__main__':

    # Create a database engine
    engine = create_engine('sqlite:///../instance/db.sqlite')  # Adjust the URI based on your actual database location
    
    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()
    test = run_data_processor(session)
    print(test)
    print(test[0]['studies'])

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


def returnEmail(user_id):
    study_instance = db.session.query(Study).get(user_id)
    
    if study_instance:
        user_instance = db.session.query(User).get(study_instance.user_id)
        if user_instance:
            return user_instance.email

    return None



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