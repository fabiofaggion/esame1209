import sqlite3

# Function to get all client-trainer associations
def get_client_trainer_associations():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query to select all client-trainer associations
    sql = 'SELECT * FROM client_trainer'
    cursor.execute(sql)
    associations = cursor.fetchall()

    cursor.close()
    conn.close()

    return associations

# Function to add a new client-trainer association
def add_client_trainer_association(association):
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    # SQL to insert a new client-trainer association
    sql = 'INSERT INTO client_trainer(client_id, trainer_id) VALUES(?, ?)'

    try:
        cursor.execute(sql, (association['client_id'], association['trainer_id']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

# Function to get a client-trainer association by client ID
def get_client_trainer_by_client_id(client_id):
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query to select a client-trainer association by client ID
    sql = 'SELECT * FROM client_trainer WHERE client_id = ?'
    cursor.execute(sql, (client_id,))
    association = cursor.fetchone()

    cursor.close()
    conn.close()

    return association
