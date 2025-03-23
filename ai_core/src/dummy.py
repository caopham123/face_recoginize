# import json
# with open('ai_core/dataset/dummy.json', 'r',encoding='utf-8') as file:
#     data = json.load(file)
import pandas as pd
path = 'ai_core/dataset/dummy.json'
df = pd.read_json(path)
print(df)

# idx = 1
# df['id']