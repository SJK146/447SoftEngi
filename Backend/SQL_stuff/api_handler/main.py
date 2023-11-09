from flask import Flask
from data_processor import run_data_processor
# from api_handler import handle_api_requests
from flask_sqlalchemy import SQLAlchemy
from ....project.models import db, User, Study, Tests 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'the_secret_key'

db.init_app(app)

if __name__ == '__main__':
    
    run_data_processor(db)
    # handle_api_requests()
