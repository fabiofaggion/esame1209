import sqlite3
import datetime


def get_db_connection():
    conn = sqlite3.connect('db/database.db')  # Adjust this path if needed
    conn.row_factory = sqlite3.Row
    return conn


def add_workout(workout):
    """
    Adds a new workout to the database.

    :param workout: A dictionary containing workout details.
    :return: True if the workout was successfully added, False otherwise.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    success = False

    # SQL command to insert a new workout
    sql = '''
        INSERT INTO Workouts (title, description, level, type, date)
        VALUES (?, ?, ?, ?, ?)
    '''
    try:
        # Execute the SQL command with workout details
        cursor.execute(sql, (workout['title'], workout['description'], workout['Level'], workout['type'], workout['date']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR:', str(e))
        conn.rollback()  # Roll back any changes if there's an error
    finally:
        cursor.close()
        conn.close()

    return success

def get_workouts():
    """
    Fetches all workouts from the database.

    :return: A list of workouts.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL command to select all workouts
    sql = 'SELECT * FROM Workouts ORDER BY date DESC'
    cursor.execute(sql)
    workouts = cursor.fetchall()

    cursor.close()
    conn.close()

    return workouts