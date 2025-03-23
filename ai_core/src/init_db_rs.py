import pandas as pd
from setting import DB_RESULT_PATH

df = pd.DataFrame({
    "email": [],
    "name": [],
    "time": []
})
df.to_json(DB_RESULT_PATH)