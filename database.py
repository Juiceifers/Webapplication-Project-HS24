import sqlite3

def create_connection():
    conn = sqlite3.connect('users.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        maps TEXT
                        )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS maps (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        map_name TEXT NOT NULL,
                        files TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def add_user(username, password):
    maps = ""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, maps) VALUES (?, ?, ?)', (username, password, maps))
    conn.commit()
    conn.close()

def get_user(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def add_map(map_name, user_name, files):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (user_name, ))
    user_entry = cursor.fetchone()

    user_maps = user_entry[3]
    user_id = user_entry[0]

    cursor.execute('INSERT INTO maps (map_name, user_id, files) VALUES (?, ?, ?)', (map_name, user_id, files))

    ""
    "12 24 1"
    "12 24 1 5"
            
    

    if user_maps == "":
        new_maps = map_name
    else:
        new_maps = " ".join(user_maps.split() + [map_name])

    print("NEW MAPS:", new_maps)

    cursor.execute('UPDATE users SET maps = ? WHERE id = ?', (new_maps, user_id))

    conn.commit()
    conn.close()

#def get_user_maps(user_id):


def get_maps(map_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM maps WHERE map_id = ?', (map_id))
    user = cursor.fetchone()
    conn.close()
    return user
