import psycopg2
import numpy as np

DB_NAME = "db_employee"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_HOST = "127.0.0.1"
DB_PORT = 5433


class QueryMember:
    def get_db_connection(self):
        try:
            conn = psycopg2.connect(database=DB_NAME, user= DB_USER, 
                                    password= DB_PASS, host= DB_HOST, port=DB_PORT)
            return conn
        except Exception as e:
            raise e

    def validate_id(self, id: int):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM member WHERE id=%s", (id,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if row is not None:
                return True
            return False
        except Exception as e: raise e

    def validate_email(self, email: str):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM member WHERE lower(email)=%s", (email.lower(),))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if row is None: # Not found email
                return True
            return False    # Found email
        except Exception as e: raise e

    def create_member(self, full_name, email, face: np.ndarray):
        try:
            #======== Convert numpy.ndarray into list
            vector_embedding = face.tolist()
            #======== Execute query
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO member (full_name, email, face_embedding) VALUES
                (%s, %s, %s)
                """, (full_name, email, vector_embedding))
            conn.commit()
            cursor.close()
            conn.close()
            return True

        except Exception as e:
            raise e

    def update_member(self, id: int, full_name=None, email=None, face:np.ndarray=None):
        try:

            face_embedding = None  # Initialize as None
            conn = self.get_db_connection()
            cursor = conn.cursor()

            query_string = "UPDATE member SET "
            updates = []
            query_params = []

            if full_name is not None:
                updates.append("full_name = %s")
                query_params.append(full_name)
                
            if email is not None:
                updates.append("email = %s")
                query_params.append(email)
                
            if face is not None:
                face_embedding = face.tolist()  # Convert numpy array to list if needed
                updates.append("face_embedding = %s")
                query_params.append(face_embedding)

            # Check if we have any fields to update
            if not updates:
                raise ValueError("No fields to update")

            query_string += ", ".join(updates)
            query_string += " WHERE id = %s"
            query_params.append(id)

            # Execute the query
            cursor.execute(query_string, query_params)
            conn.commit()  # Don't forget to commit!
            cursor.close()
            conn.close()
        except Exception as e:
            raise e
   
    def check_member(self,id, full_name, email, time_checking):
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO member_checking (id, full_name, email, time_checking) VALUES
                (%s, %s, %s, %s)
                """, (id, full_name, email, time_checking))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            raise e
        
    def get_member_list(self):
        try: 
            conn = self.get_db_connection()
            cursor= conn.cursor()
            cursor.execute("SELECT id, full_name, email, face_embedding FROM member")
            rows = cursor.fetchall()

            for row in rows:
                if row[3] is not None:
                    print(f"id: {row[0]} - name: {row[1]} - email: {row[2]}- face_embbedding {True}")
                else:
                    print(f"id: {row[0]} - name: {row[1]} - email: {row[2]}- face_embedding {False}")
            cursor.close()
            conn.close()
        except Exception as e:
            raise e
        
    def delete_member(self, id):
        try: 
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM member WHERE id=%s;
                """, (id,))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            raise e

if __name__ == "__main__":
    dbConn = QueryMember()
    dbConn.get_db_connection()
    # dbConn.get_member_list()

    # dbConn.create_member('member01', 'member01@gmail.com')
    # dbConn.delete_member(1)
    # dbConn.delete_member(4)
    dbConn.get_member_list()