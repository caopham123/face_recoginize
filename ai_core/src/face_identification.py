import numpy as np
from .setting import DB_FACE_PATH, FACE_RECOGNITION_THRESHOLD
import pandas as pd
from numpy.linalg import norm
import datetime
from api.helpers.db_connection import QueryMember

def cosine_similarity(emb1, emb2):
    return np.dot(emb1, emb2) / (norm(emb1) * norm(emb2))

class FaceIdentification:
    def get_result(self, input_embedding:np.ndarray):
        if input_embedding is None:
            return None
        dbConn = QueryMember()
        conn = dbConn.get_db_connection()
        cursor = conn.cursor()
        query_face_embedding = """
                        SELECT id, full_name, email, 1 - (face_embedding <=> %s::vector) as cosine_similarity 
                        FROM member
                        WHERE 1 - (face_embedding <=> %s::vector) > %s
                        ORDER BY cosine_similarity LIMIT 1; 
                       """
        cursor.execute(query_face_embedding, (input_embedding.tolist(),input_embedding.tolist(), FACE_RECOGNITION_THRESHOLD))
        result = cursor.fetchone()

        if result is None: 
            cursor.close()
            return None
        
        # query_checking_event = ""

        dbConn.check_member(result[0], result[1], result[2])
        return {"id": result[0], "email": result[2], "full_name": result[1]}

     
