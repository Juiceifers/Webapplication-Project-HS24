import sqlite3
import os

def create_connection():
    try:
        # Get the current directory where the script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Create a 'data' directory in the current directory
        data_dir = os.path.join(current_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        # Create the database file path
        db_path = os.path.join(data_dir, 'users.db')
        print(f"Database path: {db_path}")  # Debug print
        
        # Create and return the connection
        conn = sqlite3.connect(db_path)
        return conn
    except Exception as e:
        print(f"Error in create_connection: {e}")
        raise e

def create_table():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )''')
        
        # Create maps table
        cursor.execute('''CREATE TABLE IF NOT EXISTS maps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            map_name TEXT NOT NULL,
            files TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
        
        conn.commit()
        print("Database tables created successfully")
        
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise e
    finally:
        conn.close()

def add_user(username, password):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                      (username, password))
        conn.commit()
        print(f"User {username} added successfully")
        return True
        
    except Exception as e:
        print(f"Error adding user: {e}")
        return False
    finally:
        conn.close()

def get_user(username):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        print(f"Retrieved user {username}: {'Found' if user else 'Not found'}")
        return user
        
    except Exception as e:
        print(f"Error getting user: {e}")
        return None
    finally:
        conn.close()

def add_map(map_name, user_name, files):
    print("\n=== Starting add_map operation ===")
    print(f"Attempting to add map: {map_name} for user: {user_name}")
    
    conn = create_connection()
    cursor = conn.cursor()
    try:
        # Get user ID
        print("Looking up user ID...")
        cursor.execute('SELECT id FROM users WHERE username = ?', (user_name,))
        user = cursor.fetchone()
        
        if not user:
            print(f"ERROR: User {user_name} not found in database")
            return False
            
        user_id = user[0]
        print(f"Found user ID: {user_id}")
        
        # Insert new map
        print(f"Inserting map into database...")
        cursor.execute('''INSERT INTO maps (user_id, map_name, files) 
                         VALUES (?, ?, ?)''', (user_id, map_name, files))
        
        # Verify the insertion
        map_id = cursor.lastrowid
        print(f"Map inserted with ID: {map_id}")
        
        conn.commit()
        print("Database changes committed successfully")
        
        # Verify the map was added
        cursor.execute('SELECT * FROM maps WHERE id = ?', (map_id,))
        added_map = cursor.fetchone()
        print(f"Verification - Added map: {added_map}")
        
        return True
        
    except Exception as e:
        print(f"ERROR in add_map: {str(e)}")
        print(f"Error type: {type(e)}")
        return False
    finally:
        conn.close()
        print("=== Finished add_map operation ===\n")

def get_user_maps(user_id):
    print("\n=== Starting get_user_maps operation ===")
    print(f"Fetching maps for user_id: {user_id}")
    
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM maps WHERE user_id = ?', (user_id,))
        maps = cursor.fetchall()
        print(f"Found {len(maps)} maps: {maps}")
        return maps
    except Exception as e:
        print(f"ERROR in get_user_maps: {str(e)}")
        return []
    finally:
        conn.close()
        print("=== Finished get_user_maps operation ===\n")

# Initialize database when the module is imported
def create_table():
    try:
        create_table()
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        
def debug_database_state():
    print("\n=== Database State Debug ===")
    conn = create_connection()
    cursor = conn.cursor()
    try:
        # Check users table
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        print(f"Users in database: {users}")
        
        # Check maps table
        cursor.execute('SELECT * FROM maps')
        maps = cursor.fetchall()
        print(f"Maps in database: {maps}")
        
    except Exception as e:
        print(f"ERROR in debug_database_state: {str(e)}")
    finally:
        conn.close()
        print("=== End Database State Debug ===\n")