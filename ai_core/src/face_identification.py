import numpy as np
from .setting import DB_FACE_PATH, FACE_RECOGNITION_THRESHOLD
import pandas as pd
from numpy.linalg import norm
import datetime
from api.helpers.db_connection import QueryMember

def cosine_similarity(emb1, emb2):
    return np.dot(emb1, emb2) / (norm(emb1) * norm(emb2))

class FaceIdentification:

    def get_result(self, input_embedding):
        dbConn = QueryMember()
        cursor = dbConn.get_db_connection().cursor()
        query_string = """
                        SELECT id, full_name, email FROM employee
                        ORDER BY face_embedding <=> %s::vector
                        LIMIT 1; 
                       """
        cursor.execute(query_string, (input_embedding,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            now = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
            dbConn.check_member(result[0], result[1], result[2], now)
            return {"id": result[0], "email": result[2], "name": result[1], "time_checking": result[3]}
        else: return {"id": None, "email": None, "name": None, "time_checking": None}        
