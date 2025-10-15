import sqlite3


def add_new_stats(input_data, date, status):
    connection = sqlite3.connect('statis.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS forecasts (
    id INTEGER PRIMARY KEY,
    input_data TEXT NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL
    )
    ''')

    cursor.execute('INSERT INTO forecasts (input_data, date, status) '
                   'VALUES (?, ?, ?)', (input_data, date, status))

    connection.commit()
    connection.close()