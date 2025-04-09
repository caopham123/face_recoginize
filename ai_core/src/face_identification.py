import numpy as np
from .setting import DB_FACE_PATH, FACE_RECOGNITION_THRESHOLD
import pandas as pd
from numpy.linalg import norm
import datetime

def cosine_similarity(emb1, emb2):
    return np.dot(emb1, emb2) / (norm(emb1) * norm(emb2))

class FaceIdentification():
    def __init__(self):
        self.db = pd.read_json(DB_FACE_PATH)
        self.ids = self.db["id"].to_numpy().tolist()
        self.names = self.db["name"].to_numpy().tolist()
        self.emails = self.db["email"].to_numpy().tolist()
        self.faces = self.db["face"].to_numpy().tolist()
        
    def get_result(self, target_embedding):
        old_thresh = 0
        index = -1

        for idx, item in enumerate(self.faces):
            cosine = cosine_similarity(item, target_embedding)
            print(f"cosine with input img and exist img {cosine}")
            if cosine > old_thresh and cosine > FACE_RECOGNITION_THRESHOLD:
                index = idx
        
        if index == -1:
            return {"id": None, "email": None, "name": None, "time_checking": None}
        now = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
        return {"id": self.ids[index], "email":self.emails[index], "name": self.names[index], "time_checking": now}
        
