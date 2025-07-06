import psycopg2

DB_NAME = "db_employees"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_HOST = "127.0.0.1"
DB_PORT = 5432


class DBConnection:
    def get_db_connection(self):
        try:
            conn = psycopg2.connect(database=DB_NAME, user= DB_USER, 
                                    password= DB_PASS, host= DB_HOST, port=DB_PORT)
            return conn
        except Exception as e:
            raise e

    def create_member(self, full_name, email):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO employee (full_name, email) VALUES
                (%s, %s)
                """, (full_name, email))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            raise e
        
    def get_member_list(self):
        try: 
            conn = self.get_db_connection()
            cursor= conn.cursor()
            cursor.execute("SELECT id, full_name, email FROM employee")
            rows = cursor.fetchall()

            for row in rows:
                print(f"id: {row[0]} - name: {row[1]} - email: {row[2]}")
            cursor.close()
            conn.close()
        except Exception as e:
            raise e
        
    def update_member(self, id, full_name, email):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(""" 
                UPDATE employee SET full_name=%s, email= %s
                WHERE id=%s
                """, (full_name, email, id))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            raise e
        
    def delete_member(self, id):
        try: 
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM employee WHERE id=%s;
                """, (id,))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            raise e

if __name__ == "__main__":
    dbConn = DBConnection()
    dbConn.get_db_connection()
    # dbConn.get_member_list()

    dbConn.create_member('member01', 'member01@gmail.com')
    # dbConn.delete_member(1)
    # dbConn.delete_member(2)
    dbConn.get_member_list()