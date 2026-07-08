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

def get_user_id_by_username():
    username = input("search username:")
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        row = cur.fetchone()
        conn.close()

        if row:
            return row[0]
        
        else:
            print("username not found please try again")
            return None
        

#user functions
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

#post functions:
def create_post():
    user_id = get_user_id_by_username()
    if user_id is None:
        return
    title = input("Post title:")
    body = input("Post body:")
    publish = input("publish now? (y/n): ")
    published = publish.lower() == "y"


    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO posts (title, body, published) VALUES(%s, %s, %s, %s) RETURNING id", (title, body, publish, published)
        )
        row = conn.fetchone()
        conn.close()
        conn.commit()
    
        print(f"post #{row[0]} created.")
    