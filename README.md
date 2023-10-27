# 447SoftEngi

Should just need python to run back end
all front end code is inside the project folder currently and has a seperate read me to run the program.

	pip install fastapi unicorn 

	pip install requests 

*maybe something else, I've got a preconfigured venv so I dont remember everything that it has. 

start with 

	uvicorn main:app --reload

loads the page on localhost port 8000 or http://localhost:8000

check out the extensions below for free documentation 

	/docs
	/redoc

rename main.py->  to anything else and othermain.py-> main.py and rerun to see a different way of doing the html (I perfer the inital but the latter is nice for small pages) 



## SQL NOTES

 Install:
 	
  	sudo apt-get install sqlite3

Open:

   	sqlite3 your_database_name.db
MISC:

	.list 
 	.read
  	.schema table_name
   	.exit


Create Table:

 	CREATE TABLE Users (
   		ID INTEGER PRIMARY KEY,
    		Name TEXT,
    		Email TEXT UNIQUE
	);
 Interactions:

  	INSERT INTO Users (Name, Email) VALUES ('John Doe', 'john@example.com');
	SELECT * FROM Users WHERE Name = 'John Doe';
	UPDATE Users SET Email = 'newemail@example.com' WHERE Name = 'John Doe';
	DELETE FROM Users WHERE Name = 'John Doe';


	
