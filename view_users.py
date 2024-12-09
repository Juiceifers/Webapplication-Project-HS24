import sqlite3

def view_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

if __name__ == "__main__":
    users = view_users()
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Password: {user[2]}")