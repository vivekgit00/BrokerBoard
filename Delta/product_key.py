import requests
import json
responce = requests.get("https://api.delta.exchange/v2/products")
data = responce.json()['result']
# print(data.keys())
results = []
data_dict = {}
for data in data:
    print(str(data['id'])+ " " + data['symbol'])
    results.append({data['symbol']: data['id']})

with open('dict_files\\product_key.json', 'w') as f:
    json.dump(results, f)