#--- data --- 
import psycopg 
DB_NAME = "blog_db"

def get_connection():
    return psycopg.connect(f"dbname={DB_NAME}")

def new_user():
    username = input("Username:")
    email = input("Email:")

    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO users (username, email) VALUES(%s, %s)", (username, email))
    conn.commit()
    conn.close()

def list_users():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users;")
        rows = cur.fetchall()
        for row in rows:
            print(row)

    conn.close()

def search_user():
    term = input("seach for username:")
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE username = %s", (term,))
        row = cur.fetchone()
        print (row)
        conn.close()

def delete_user():
    deleted = input("Username to delete:")
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM users WHERE username = %s RETURNING username", (deleted,))
        row = cur.fetchone()

        if row:
            print(f"User '{row[0]}' was deleted.")
        else:
            print(f"No user found with username '{deleted}'.")
    conn.commit()
    conn.close()