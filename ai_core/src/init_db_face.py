import pandas as pd
from setting import DB_FACE_PATH

df = pd.DataFrame({
    "id": [], 
    "name": [],
    "email": [],
    "face": []
})
df.to_json(DB_FACE_PATH)
# print("WRITE TO JSON FILE")