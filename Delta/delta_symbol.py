import json
# with open('../dict_files/delta_symbols.json', 'r') as f:
#     symbols = json.load(f)
#
# print(symbols)



import requests, json
symbols = set()
headers = {
    'Accept': 'application/json'
}

response = requests.get('https://api.india.delta.exchange/v2/tickers', headers=headers)

if response.status_code == 200:
    tickers = response.json()
    symbol = tickers['result']
    n = 1
    for i in symbol:
        symbols.add(i['symbol'])
        n+=1
        print(n)
    with open('../dict_files/delta_symbols.json', 'w') as f:
        json.dump(list(symbols), f)
else:
    print(f"Failed to fetch data: {response.status_code}")
