import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import Study
from models import Study

# Create a database engine
engine = create_engine('sqlite:///../instance/db.sqlite')  # Adjust the URI based on your actual database location

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Query data from the database
results = session.query(Study).all()

# Process the results
for result in results:
    print(f"Study ID: {result.id}")
    print(f"User ID: {result.user_id}")
    print(f"Ticker: {result.ticker}")
    print(f"Studies: {result.studies}")
    print("------")

# Close the session when done
session.close()
