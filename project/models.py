from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
import json

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase, MappedAsDataclass):
    pass

db = SQLAlchemy()

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(250), unique=True, nullable=False)
	name = db.Column(db.String(250))
	password = db.Column(db.String(250), nullable=False)
	#phone = db.

@event.listens_for(User.__table__, 'after_create')
def initaliaze_user(*args, **kwargs):
	db.session.add(User(id=1, email='bob@bob.com', name='Bob', password='scrypt:32768:8:1$Gt3t4ETVJR1eb6Fh$0822fe5f6df875a78ca7f58a106251f470377096656e1929f4d0aee473452e84e540afb90316885822fb87a88543ad750ae59972875f0448a2774135c0a1bd2f'))
	db.session.commit()
	
class Study(UserMixin, db.Model): #ie a user 'studies a stock
	id=db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	ticker = db.Column(db.Integer, nullable=False)
	studies = db.Column(db.Text, nullable=True)
	historical_data = db.Column(db.Text, nullable=True)
	results = db.Column(db.Text, nullable=True)
	#studies ex: "metric:threshold, metric2:threshold2"  Parse when calling api
	#Results listed in Text, format same "metric:value, metric2:value" Parse when displaying to frontend
	input_1 = db.Column(db.String(255))
	input_2 = db.Column(db.String(255))
	input_3 = db.Column(db.String(255))


class Tests(UserMixin, db.Model):
	id=db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	results=db.Column(db.Text, nullable=True)

# class Metric(UserMixin, db.Model):#loop through yf ticker.info.* to get list of metrics
# 	id=db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(50))

#id, {metric: 30.0}

# class HistoricalData(UserMixin, db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	ticker = db.Column(db.String(250), nullable=False)


# class Studied(UserMixin, db.Model):
# 	# Results table 
#     id = db.Column(db.Integer, primary_key=True)
#     study_id = db.Column(db.Integer, db.ForeignKey("study.id"), nullable=False)
#     metric_id = db.Column(db.Integer, db.ForeignKey("metric.id"), nullable=False)
	
class Test(db.Model):#loop through yf ticker.info.* to get list of metrics
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    formula = db.Column(db.String(50))
    n_inputs = db.Column(db.Integer, nullable=False)
    input_name_1 = db.Column(db.String(50))
    input_name_2 = db.Column(db.String(50))
    input_name_3 = db.Column(db.String(50))
	
@event.listens_for(Test.__table__, 'after_create')
def initaliaze_test(*args, **kwargs):
	db.session.add(Test(id=1, name='CCI', n_inputs=2, input_name_1='Interval', input_name_2='Time Period', input_name_3=None))
	db.session.add(Test(id=2, name='SMA', n_inputs=3, input_name_1='Interval', input_name_2='Time Period', input_name_3='Series Type'))
	db.session.add(Test(id=3, name='EMA', n_inputs=3, input_name_1='Interval', input_name_2='Time Period', input_name_3='Series Type'))
	db.session.add(Test(id=4, name='RSI', n_inputs=3, input_name_1='Interval', input_name_2='Time Period', input_name_3='Series Type'))
	db.session.add(Test(id=5, name='OHLC', n_inputs=2, input_name_1='Interval', input_name_2='Time Period', input_name_3=None))
	db.session.commit()

class StudyTest( db.Model): #This is the thing that the metric studies
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	study_id = db.Column(db.Integer, db.ForeignKey("study.id"), nullable=False)
	test_id = db.Column(db.Integer, db.ForeignKey("test.id"), nullable=False)
	input_1 = db.Column(db.Integer)
	input_2 = db.Column(db.Integer)
	input_3 = db.Column(db.Integer)
	chart = db.Column(db.Integer)

#ok so the layout for what needs to go in the database
#-user credentials tagged to their individual data
#
#          -the stocks they are following which will have a                study group attached to it.
#
#          -the study groups they create which can then be            added to the stocks they want to follow
#
#  -the data we collect for stocks can be stored seperately to potentially reduce the amount calls if we actually had multiple users. with this data we can check if there has already been a call or two that day for that stock to limit the amount of calls.
#i kind of explained that poorely let me know if you want a clearer picture
#Shmitty — Yesterday at 6:31 PM
#I think this covers most of the data
#But we need to specify more of the specific user values
#blacknight94 — Yesterday at 6:32 PM
#but yes most likely each stock will have different metrics they are following
#DanielF — Yesterday at 6:35 PM
#Ok. So each stock should have a study group.  I assume each metric has a threshold that goes along with the study.  Besides that I am storing username, password, id, and email.
#I should probably add a result parameter in the database so it can determine when to send the email or let the user know
#Shmitty — Yesterday at 6:38 PM
#I’m not sure how sql is structured, but could we have a column that stores a data structure? 
#DanielF — Yesterday at 6:38 PM
#I assume so.  Let me check
#Shmitty — Yesterday at 6:39 PM
#And store the comparison/I put metrics in that instead of over a few rows
#DanielF — Yesterday at 6:47 PM
#I can store the data structure in another table and just associate that with the ID of the user account table. So there will be 2 tables in the database and one will store user info and the other the study groups.
#Shmitty — Yesterday at 6:50 PM
#That might be the way to go, it depends on how we choose to allow for the user to customize the tests
#DanielF — Yesterday at 6:53 PM
#For the front-end we should decide how the process for how the user selects the studies and stocks so we can integrate this easier.
