import sqlite3

# Function to get all clients
def get_clients():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query to select all clients
    sql = 'SELECT * FROM clients'
    cursor.execute(sql)
    clients = cursor.fetchall()

    cursor.close()
    conn.close()

    return clients

# Function to add a new client
def add_client(client):
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    # SQL to insert a new client
    sql = 'INSERT INTO clients(user_id) VALUES(?)'

    try:
        cursor.execute(sql, (client['user_id'],))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

# Function to get a client by ID
def get_client_by_id(id):
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query to select a client by ID
    sql = 'SELECT * FROM clients WHERE id = ?'
    cursor.execute(sql, (id,))
    client = cursor.fetchone()

    cursor.close()
    conn.close()

    return client
