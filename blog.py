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

def search_post_title():
    post = input("post title: ")
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM posts WHERE title = %s", (post,))
        rows = cur.fetchall()
        for row in rows:
            print(row)
        conn.close()


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
            "INSERT INTO posts (title, body, published, user_id) VALUES (%s, %s, %s, %s) RETURNING id", (title, body, published, user_id)
        )
        row = cur.fetchone()
        conn.commit()
        conn.close()
    
    
        print(f"post #{row[0]} created.")

def list_posts():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM posts;")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    conn.close()

def delete_post():
    deleted = input("post to delete: ")
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM posts WHERE id = %s RETURNING title", (deleted,))
        row = cur.fetchone()

        if row:
            print(f"Post '{row[0]}' was deleted.")
        
        else:
            print(f"post '{deleted}' was not found.")
    conn.commit()
    conn.close()

#comment functions 
def make_comment():
    user_id = get_user_id_by_username()
    if user_id == None:
        print("no user found. please try again.")
        return
    list_posts() #hard part for this is going to be linking two foreign keys at once, user id and post id.
    post_id = input("enter id of the would you like to comment on:")
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT title FROM posts WHERE id = %s", (post_id,))
        row = cur.fetchone()

        if row:
            print(f"'{post_id}' was chosen.")
            body = input("type comment:")
            cur.execute("INSERT INTO comments (post_id, user_id, body) VALUES (%s, %s, %s)", (post_id, user_id, body))
        else:
            print("post was not found :( ")

    conn.commit()
    conn.close()

def list_comments():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM comments;")
        rows = cur.fetchall()
        for row in rows:
            print(row)
        conn.close()