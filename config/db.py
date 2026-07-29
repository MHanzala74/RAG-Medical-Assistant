from dotenv import load_dotenv
import psycopg2
import os
import hashlib

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("POSTGRES_USERNAME"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT"),
        sslmode="require"
    )

def create_table(username: str, password: str, role: str):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role VARCHAR(50) NOT NULL
            );
        """)

        conn.commit()
        print("User inserted successfully")

    except Exception as e:
        print(f"DB ERROR: {e}")

    finally:
        cur.close()
        conn.close()

def get_user_by_username(username:str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT username, password, role FROM users WHERE username=%s",
        (username,)
    )
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return{
            "username":user[0],
            "password":user[1],
            "role":user[2]
        }
    return None


def create_user(username:str,password:str,role:str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (username,password,role) VALUES (%s, %s, %s)",
        (username,password,role)
    )

    conn.commit()
    cur.close()
    conn.close()