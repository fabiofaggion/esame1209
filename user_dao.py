import sqlite3

def get_db_connection():
    # Usa un percorso relativo per facilitare lo spostamento del progetto
    connection = sqlite3.connect('database/database.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_user_by_id(id_utente):
    query = 'SELECT * FROM users WHERE id = ?'
    
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, (id_utente,))
        result = cursor.fetchone()
        
    return result

def get_user_by_username(username):
    query = 'SELECT * FROM users WHERE username = ?'
    
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        
    return result

def create_user(nuovo_utente):
    query = 'INSERT INTO users(username, password, name, role) VALUES (?, ?, ?, ?)'

    success = False
    with get_db_connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query, (nuovo_utente['username'], nuovo_utente['password'], nuovo_utente['name'], nuovo_utente['role']))
            connection.commit()
            success = True
        except Exception as e:
            print('Error:', str(e))
            connection.rollback()

    return success





# import sqlite3



# # Function to get a user by ID
# def get_user_by_id(id_utente):
#     query = 'SELECT * FROM users WHERE id = ?'
    
#     connection = sqlite3.connect('C:/Users/Fabio/Desktop/flask/esame1209/database/database.db')

#     connection.row_factory = sqlite3.Row
#     cursor = connection.cursor()

#     cursor.execute(query, (id_utente,))
#     result = cursor.fetchone()
    
#     cursor.close()
#     connection.close()

#     return result

# # Function to get a user by username
# def get_user_by_username(username):
#     query = 'SELECT * FROM users WHERE username = ?'
    
#     connection = sqlite3.connect('C:/Users/Fabio/Desktop/flask/esame1209/database/database.db')

#     connection.row_factory = sqlite3.Row
#     cursor = connection.cursor()

#     cursor.execute(query, (username,))
#     result = cursor.fetchone()
    
#     cursor.close()
#     connection.close()

#     return result

# # Function to create a new user
# def create_user(nuovo_utente):
#     query = 'INSERT INTO users(username, password, user_type) VALUES (?, ?, ?)'

#     connection = sqlite3.connect('C:/Users/Fabio/Desktop/flask/esame1209/database/database.db')

#     connection.row_factory = sqlite3.Row
#     cursor = connection.cursor()

#     success = False

#     try:
#         cursor.execute(query, (nuovo_utente['username'], nuovo_utente['password'], nuovo_utente['user_type']))
#         connection.commit()
#         success = True
#     except Exception as e:
#         print('Error:', str(e))
#         connection.rollback()

#     cursor.close()
#     connection.close()

#     return success
