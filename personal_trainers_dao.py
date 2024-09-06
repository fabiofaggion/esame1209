import sqlite3

# Function to get all personal trainers
def get_personal_trainers():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query to select all personal trainers
    sql = 'SELECT * FROM personal_trainers'
    cursor.execute(sql)
    personal_trainers = cursor.fetchall()

    cursor.close()
    conn.close()

    return personal_trainers

# Function to add a new personal trainer
def add_personal_trainer(trainer):
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    # SQL to insert a new personal trainer
    sql = 'INSERT INTO personal_trainers(user_id, rating) VALUES(?, ?)'

    try:
        cursor.execute(
            sql, (trainer['user_id'], trainer['rating']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

# Function to get a personal trainer by ID
def get_personal_trainer_by_id(id):
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query to select a personal trainer by ID
    sql = 'SELECT * FROM personal_trainers WHERE id = ?'
    cursor.execute(sql, (id,))
    trainer = cursor.fetchone()

    cursor.close()
    conn.close()

    return trainer
