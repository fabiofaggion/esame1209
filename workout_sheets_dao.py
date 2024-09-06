import sqlite3

# Function to get all workout sheets
def get_workout_sheets():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query to select all workout sheets
    sql = 'SELECT * FROM workout_sheet'
    cursor.execute(sql)
    workout_sheets = cursor.fetchall()

    cursor.close()
    conn.close()

    return workout_sheets

# Function to add a new workout sheet
def add_workout_sheet(sheet):
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    # SQL to insert a new workout sheet
    sql = 'INSERT INTO workout_sheet(client_id, trainer_id, workout_id, created_at) VALUES(?, ?, ?, ?)'

    try:
        cursor.execute(sql, (sheet['client_id'], sheet['trainer_id'], sheet['workout_id'], sheet['created_at']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

# Function to get a workout sheet by ID
def get_workout_sheet_by_id(id):
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query to select a workout sheet by ID
    sql = 'SELECT * FROM workout_sheet WHERE id = ?'
    cursor.execute(sql, (id,))
    sheet = cursor.fetchone()

    cursor.close()
    conn.close()

    return sheet
