import sqlite3

# Function to get all worksheet ratings
def get_worksheet_ratings():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query to select all worksheet ratings
    sql = 'SELECT * FROM worksheet_rating'
    cursor.execute(sql)
    ratings = cursor.fetchall()

    cursor.close()
    conn.close()

    return ratings

# Function to add a new worksheet rating
def add_worksheet_rating(rating):
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    # SQL to insert a new worksheet rating
    sql = 'INSERT INTO worksheet_rating(sheet_id, rating) VALUES(?, ?)'

    try:
        cursor.execute(sql, (rating['sheet_id'], rating['rating']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

# Function to get a worksheet rating by ID
def get_worksheet_rating_by_id(id):
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query to select a worksheet rating by ID
    sql = 'SELECT * FROM worksheet_rating WHERE id = ?'
    cursor.execute(sql, (id,))
    rating = cursor.fetchone()

    cursor.close()
    conn.close()

    return rating
