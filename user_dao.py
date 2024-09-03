import sqlite3

# Function to get a user by ID
def get_user_by_id(id_utente):
    query = 'SELECT * FROM utenti WHERE id = ?'
    
    connection = sqlite3.connect('db/database.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query, (id_utente,))
    result = cursor.fetchone()
    
    cursor.close()
    connection.close()

    return result

# Function to get a user by username
def get_user_by_username(username):
    query = 'SELECT * FROM utenti WHERE username = ?'
    
    connection = sqlite3.connect('db/database.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query, (username,))
    result = cursor.fetchone()
    
    cursor.close()
    connection.close()

    return result

# Function to create a new user
def create_user(nuovo_utente):
    query = 'INSERT INTO utenti(username, password, user_type) VALUES (?, ?, ?)'

    connection = sqlite3.connect('db/database.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    success = False

    try:
        cursor.execute(query, (nuovo_utente['username'], nuovo_utente['password'], nuovo_utente['user_type']))
        connection.commit()
        success = True
    except Exception as e:
        print('Error:', str(e))
        connection.rollback()

    cursor.close()
    connection.close()

    return success
