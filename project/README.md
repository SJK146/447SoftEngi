# 447_proj

This branch has a dropdown form that displays inputs for all the available tests the user can choose from. The form depends on the database table 'test' having some tests defined in order to know what to display on the form - I included the file test_def.txt to populate it. It also imports the user Bob, bob@bob.com, with password asdf

If you start flask with no sql.db file so it creates a new one, you can then run sqlite3 project/instance/db.sqlite < project/study_def.sql from the root dir of the repo to import the tests

pip install -r requirements.txt

`FLASK_DEBUG=1 FLASK_APP=main flask run` from project directory

note that requirements.txt has older versions of flask and werkzeug because https://github.com/maxcountryman/flask-login/issues/805

