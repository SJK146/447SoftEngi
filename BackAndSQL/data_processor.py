# The data processor, called from main.py queries the Study Table in the database and parses it into a list to send to the api_handler
from ....project.models import db, User, Study, Tests


def run_data_processor(db):
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
