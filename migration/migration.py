import psycopg2
DB_NAME = "db_employee"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_HOST = "127.0.0.1"
DB_PORT = 5433

try:
    conn = psycopg2.connect(database=DB_NAME, user= DB_USER, 
                            password= DB_PASS, host= DB_HOST, port=DB_PORT)
    cur= conn.cursor()
    cur.execute("""CREATE EXTENSION IF NOT EXISTS vector;""")
    cur.execute("""CREATE TABLE IF NOT EXISTS member( 
                    id SERIAL PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    face_embedding VECTOR(512) );
                """)
    print("Created table member successfully!")

    cur.execute("""CREATE TABLE IF NOT EXISTS checking_event( 
                    id INT NOT NULL,
                    full_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    time_checking TIMESTAMP WITH TIME ZONE DEFAULT (NOW()));
                """)
    print("Created table check_member successfully!")
    
    conn.commit()
    cur.close()
    conn.close()
except Exception as e:
    raise e