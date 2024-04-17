#db.py


import sqlite3


def create_db():
    conn = sqlite3.connect('starwars.db')
    cursor = conn.cursor()

    # Удаляем старую таблицу, если она существует
    cursor.execute('DROP TABLE IF EXISTS characters')

    # Создаем новую таблицу с актуальной схемой
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            birth_year TEXT,
            eye_color TEXT,
            films TEXT,
            gender TEXT,
            hair_color TEXT,
            height TEXT,
            homeworld TEXT,
            mass TEXT,
            name TEXT,
            skin_color TEXT,
            species TEXT,
            starships TEXT,
            vehicles TEXT,
            created TEXT,
            edited TEXT,
            url TEXT
        )
    ''')

    conn.commit()
    conn.close()