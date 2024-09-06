import sqlite3

# Function to get all workouts
def get_workouts():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query to select all workouts
    sql = 'SELECT * FROM workouts'
    cursor.execute(sql)
    workouts = cursor.fetchall()

    cursor.close()
    conn.close()

    return workouts

# Function to add a new workout
def add_workout(workout):
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    # SQL to insert a new workout
    sql = 'INSERT INTO workouts(trainer_id, title, description, level, is_public, created_at) VALUES(?, ?, ?, ?, ?, ?)'

    try:
        cursor.execute(sql, (workout['trainer_id'], workout['title'], workout['description'], workout['level'], workout['is_public'], workout['created_at']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

# Function to get a workout by ID
def get_workout_by_id(id):
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query to select a workout by ID
    sql = 'SELECT * FROM workouts WHERE id = ?'
    cursor.execute(sql, (id,))
    workout = cursor.fetchone()

    cursor.close()
    conn.close()

    return workout
