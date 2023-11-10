#untested  

import sqlite3

databaseName = 'your_database_name.db' #db name webUserInfo ??

def add_user_to_db(user_ID, username, password, num_tests, email, phone_number, authenticated, created_at):
    try:
        # Connect to the SQLite database (replace 'your_database_name.db' with your database file)
        conn = sqlite3.connect(databaseName)
        cursor = conn.cursor()

        # Insert user data into the User table
        cursor.execute(
            "INSERT INTO User (user_ID, username, password, num_tests, email, phone_number, authenticated, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (user_ID, username, password, num_tests, email, phone_number, authenticated, created_at)
        )

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

        print("User added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding user: {e}")


def add_user_data_to_db(user_ID, test_Id, integer_column, ticker, comparison):
    try:
        # Connect to the SQLite database (replace 'your_database_name.db' with your database file)
        conn = sqlite3.connect(databaseName)
        cursor = conn.cursor()

        # Insert user data into the UserData table
        cursor.execute(
            "INSERT INTO UserData (user_ID, test_Id, integer_column, ticker, comparison) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_ID, test_Id, integer_column, ticker, comparison)
        )

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

        print("User data added to UserData table successfully.")
    except sqlite3.Error as e:
        print(f"Error adding user data to UserData table: {e}")


def add_test_to_db(test_ID, name, url, type, data_location):
    try:
        # Connect to the SQLite database (replace 'your_database_name.db' with your database file)
        conn = sqlite3.connect(databaseName)
        cursor = conn.cursor()

        # Insert test data into the Tests table
        cursor.execute(
            "INSERT INTO Tests (test_ID, Name, url, type, data_location) "
            "VALUES (?, ?, ?, ?, ?)",
            (test_ID, name, url, type, data_location)
        )

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

        print("Test added to Tests table successfully.")
    except sqlite3.Error as e:
        print(f"Error adding test to Tests table: {e}")


def get_User_table_info(user_ID, column_name):
    try:
        conn = sqlite3.connect(databaseName)
        cursor = conn.cursor()

        # Ensure the column name is safe to prevent SQL injection
        allowed_columns = ['user_ID', 'username', 'password', 'num_tests', 'email', 'phone_number', 'Authenticated', 'created_at']
        if column_name not in allowed_columns:
            print("Invalid column name")
            return None
        # Construct and execute the SQL query
        query = f"SELECT {column_name} FROM User WHERE user_ID = ?"
        cursor.execute(query, (user_ID,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]  # Extract the value from the result tuple
        else:
            return None
    except sqlite3.Error as e:
        print(f"Error selecting user information: {e}")
        return None


def get_UserData_table_info(user_ID, column_name):
    try:
        conn = sqlite3.connect(databaseName)
        cursor = conn.cursor()

        # Ensure the column name is safe to prevent SQL injection
        allowed_columns = ['user_ID', 'test_Id', 'integer_column', 'ticker', 'comparison']
        if column_name not in allowed_columns:
            print("Invalid column name")
            return None
        # Construct and execute the SQL query
        query = f"SELECT {column_name} FROM UserData WHERE user_ID = ?"
        cursor.execute(query, (user_ID,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]  # Extract the value from the result tuple
        else:
            return None
    except sqlite3.Error as e:
        print(f"Error selecting user data information: {e}")
        return None


def get_Tets_table_info(test_ID, column_name):
    try:
        conn = sqlite3.connect(databaseName)
        cursor = conn.cursor()

        # Ensure the column name is safe to prevent SQL injection
        allowed_columns = ['test_ID', 'Name', 'url', 'type', 'data_location']
        if column_name not in allowed_columns:
            print("Invalid column name")
            return None

        # Construct and execute the SQL query
        query = f"SELECT {column_name} FROM Tests WHERE test_ID = ?"
        cursor.execute(query, (test_ID,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]  # Extract the value from the result tuple
        else:
            return None
    except sqlite3.Error as e:
        print(f"Error selecting test information: {e}")
        return None


