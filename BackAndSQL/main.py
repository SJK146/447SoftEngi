#TODO in main 

import API_Calls

from flask import Flask
# from data_processor import run_data_processor
# from api_handler import handle_api_requests
from flask_sqlalchemy import SQLAlchemy
from ..project.models import db, User, Study, Tests 

#email stuff 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Timer waiting 
import datetime 
import time

######
#we need an email for the email thing to work, so someone needs to create it
#it also assumes a gmail sender, so make one of those 
#####

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'database.db'
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
    
    run_data_processor()
    # handle_api_requests()

    target_time = datetime.time(7, 30)#7:30AM
    while True:
        current_time = datetime.datetime.now().time()
        if current_time >= target_time:
            break
        time.sleep(45)#sleeps for 45 seconds to put it within the exact minute to run 
    print(f"Starting db comparisons")
    time.sleep(15)

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

def send_email(recipient_email):
    subject = "Stock Trigger Notification"
    body = "Hello, your stock has hit its trigger!"
    message = MIMEMultipart()

    message["From"] = "your_email@gmail.com"
    password = "your_email_password"

    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        #Using gmail 
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()

            server.login(sender_email, password)

            server.sendmail(sender_email, recipient_email, message.as_string())

        print(f"Alert send to{recipient_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
