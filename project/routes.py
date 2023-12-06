from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Study, Test, StudyTest
import pprint, yfinance as yf
from sqlalchemy import sql
import json
import inspect
import base64
from io import BytesIO
from matplotlib.figure import Figure
import numpy
import pandas as pd
pd.set_option('display.max_rows', None)
import re
from email_validator import validate_email, EmailNotValidError


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "fpoijaf984qiub98rtbnusp9uwrnb150vmpautj"


@app.route("/")
def home():
	if current_user.is_authenticated:
		return render_template("home.html", name=current_user.name)
	else:
		return render_template("home.html")

@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method == "POST":
		new_email = request.form.get("email")
		new_name = request.form.get("name")
		new_password = request.form.get("password")
		try:
			validated = validate_email(new_email, check_deliverability=False)
			new_email = validated.normalized
		except EmailNotValidError as e:
			flash(str(e))
			return render_template("register.html")
		if not new_name:
			flash("Name is required.  Please enter your name.")
			return(render_template("register.html"))
		if not new_password:
			flash("Empty password not permitted.")
			return(render_template("register.html"))

		row = User.query.filter_by(email=new_email).first()
		if row is not None and new_email == row.email:
			flash("Email exists.  Please login")
			return redirect(url_for("login"))
		user = User(email=new_email,
					name=new_name,
					password=generate_password_hash(new_password, method='scrypt'))
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("login"))
	return render_template("register.html")

#
#
#route for the login page
@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		user = User.query.filter_by(
			email=request.form.get("email")).first()
		if not (user and check_password_hash(user.password, request.form.get("password"))):
			flash("Bad login.  Try again.")
			return redirect(url_for("studies"))
		login_user(user)
		return redirect(url_for("studies"))
	return render_template("login.html")

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))

#
#
#route for the main page that shows all a user's studygroups
#it should be called /studygroups
@app.route("/studies")
@login_required
def studies():
	studies_query = sql.text("select id, ticker, chart from study")
	studies = db.session.execute(studies_query).all()
	
	if len(studies): #there be studygroups ie studies ie things a user has chosen to study about a particular stock
		tickers = [] #yf objects for specific stock
		histories = [] #yf.history 20d table
		charts = [] #table parsed for open/close/high/low
		names = []
		studytests_list = []
		studytest_query = sql.text("""
				select 
					study.ticker AS ticker, 
					test.name AS name, 
					test.input_name_1 AS input_name_1, 
					test.input_name_2 AS input_name_2, 
					test.input_name_3 AS input_name_3,
					test.input_name_4 AS input_name_4,
					study_test.study_id AS study_test_id,
					study_test.input_1 AS input_1, 
					study_test.input_2 AS input_2, 
					study_test.input_3 AS input_3,
					study_test.input_4 AS input_4
				from 
					test, study_test, study, user 
				where 
					test.id=study_test.test_id 
					and study_test.study_id = study.id 
					and study_test.test_id = test.id
					and study.user_id = {}
				""".format(current_user.id))
		print(studytest_query)
		studytests = db.session.execute(studytest_query).all()
		print(studytests)
		studytests_list.append(studytests)
		#print(studytests_list)
		for study in studies:
			name = study.ticker
			chart = study.chart
			names.append(name)
			charts.append(chart)
		return render_template('studies.html', studies=studies, studytests=studytests, charts=charts, tickers=tickers, histories=histories, names=names, name=current_user.name)
	return render_template('studies.html', text="No Studies")

#
# this takes the inputs from the add studies page currently just has some random input boxes as proof of concept
# this is not dynamic and does not work with the drop down currently
@app.route("/add_study", methods=["GET", "POST"])
@login_required
def add_study():
	#process the form if it was submitted in this request
	if request.method == "POST":
		#print(request.form)
		if not request.form.get("ticker"): #ticker is required
			flash("Please enter a ticker symbol.")
			return redirect(url_for("add_study"))
		tkr=request.form.get("ticker")

		#generate 20d OHLC chart for ticker
		try:
			ticker = yf.Ticker(tkr)
			#put in db so it doesn't call api every load
			period = "20d"
			history = ticker.history(period)
			dates = history.index.strftime('%m/%d/%Y')
			opens = history.Open
			highs = history.High
			lows = history.Low
			closes = history.Close
			historyzip = zip(dates, lows, opens, closes, highs)
			chrt = ""
			for row in historyzip:
				chrt += str(list(row)) + ",\n"
			chrt = re.sub(r'[^\S\r\n]+', "", str(chrt).strip())
			#print(chrt)
		except:
			chrt = ""

		newStudy = Study(
			user_id=current_user.id,
			ticker=tkr,
			chart=chrt
		)
		db.session.add(newStudy)

		tests = db.session.execute(db.select(Test.id, Test.name, Test.input_name_1, Test.input_name_2, Test.input_name_3, Test.input_name_4)).all()
		print(tests)
		for i, test in enumerate(tests, start=1):
			max_inputs = 5
			#print("i is " + str(i))
			inputs = []
			chkbxname = "checkbox-" + str(i)
			#print(chkbxname)
			inputval=""
			if request.form.get(chkbxname):
				for j in range(1,max_inputs+1):
					input_name = "input-" + str(j) + "-" + str(i)
					#print(j)
					#print(input_name)
					if request.form.get(input_name):
						inputval = request.form.get(input_name)
					else:
						inputval = -1
					inputs.append(inputval)
				#print("inputs:")
				#pprint.pprint(inputs)
				newStudyTest = StudyTest(study_id = newStudy.id, 
								   test_id = test.id, 
								   input_1 = inputs[0], 
								   input_2 = inputs[1], 
								   input_3 = inputs[2],
								   input_4 = inputs[3])
				db.session.add(newStudyTest)
		#print(len(newStudyTests))

		#for newStudyTest in newStudyTests:
		#	db.session.add(newStudyTest)
		db.session.commit()
		db.session.close()
		return redirect(url_for("studies"))
	
	#otherwise generate the new study form
	#the template will loop through all the tests and generate input field 
	#for each test; input will be hidden unless that test is selected
	tests = db.session.execute(db.select(Test.name, Test.input_name_1, Test.input_name_2, Test.input_name_3, Test.input_name_4)).all()
	print(tests)
	test_names = ["input_name_1", "input_name_2", "input_name_3", "input_name_3"]

	studies = db.session.execute(
		db.select(Study, Test, StudyTest).where(Study.id==StudyTest.study_id and Test.id==StudyTest.test_id))
	n = list(range(1,4))
	db.session.close()
	return render_template('add_study.html', studies=studies, 
						test_names=test_names, n_studies=n, tests=tests)
