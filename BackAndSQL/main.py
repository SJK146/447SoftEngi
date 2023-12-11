#TODO in main 

import API_Calls

from flask import Flask
# from data_processor import run_data_processor
# from api_handler import handle_api_requests
from flask_sqlalchemy import SQLAlchemy
from ../project/project.models import db, User, Study, Tests 

#email stuff 
import smtplib
import ssl
from email.message import EmailMessage

#Timer waiting 
import datetime 
import time


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = '../project/study_def.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'the_secret_key'

db.init_app(app)


def run_data_processor():
    studies = db.session.query(Study).all()

    study_data = []
    for item in studies:
        study_data.append({
            "id": item.id,
            "user_id": item.user_id,
            "ticker": item.ticker,
            "studies": item.studies,
        })

    return study_data


def add_test_result(user_id, results_data):
    user = User.query.get(user_id)
    new_test = Tests(user=user, results=results_data)
    db.session.add(new_test)
    db.session.commit()

if __name__ == '__main__':

    study_data = run_data_processor()
    for entry in study_data:
        print(entry)

    # handle_api_requests()

    target_time = datetime.time(7, 30)#7:30AM
    while True:
        current_time = datetime.datetime.now().time()
        if current_time >= target_time:
            break
        time.sleep(45)#sleeps for 45 seconds to put it within the exact minute to run 
    print(f"Starting db comparisons")
    sleep(15)

    #get informaiton from bd, format into useful types 


    #loop iterating through data list 
        #check ticker and test, make call
        #do comparision with return 
        #notify if needed 
    


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



#python interface


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