
"""
Get spot_price symbol
"""
import json
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('https://api.india.delta.exchange/v2/indices', params={}, headers = headers)

with open('dict_files\\delta_symbols.json', 'r') as f:
    delta_symbol = json.load(f)
with open('dict_files\\product_key.json', 'r') as f:
    prodect_key = json.load(f)

data = r.json()
results = []
spot_symbol_detect = []
for d in data['result']:
    # print(d)
    spot_symbol = d['symbol']
    # print(spot_symbol[:4])
    check = spot_symbol[:4]
    dex = False
    if ".DEX" in check:
        dex = True
        spotsymbol = spot_symbol.split(".DEX")[1]
        # print(spotsymbol)
        for i in delta_symbol:
            # print(delta_symbol[i])
            if spotsymbol.upper() == i.upper():
                results.append({spot_symbol: i})
                spot_symbol_detect.append(spot_symbol)
    check_2 = spot_symbol[:3]
    if not dex:
        if ".DE" in check_2:
            spotsymbol_2 = spot_symbol.split(".DE")[1]
            # print(spotsymbol_2)
            for i in delta_symbol:
                # print(i)
                if spotsymbol_2.upper() == i.upper():
                    results.append({spot_symbol: i})
                    spot_symbol_detect.append(spot_symbol)

    if spot_symbol not in spot_symbol_detect:
        print(spot_symbol)
        # spotsymbol = spot_symbol.split(".DEX")[1]
        dex = False
        if ".DEX" in check:
            dex = True
            spotsymbol = spot_symbol.split(".DEX")[1]
            print(spotsymbol)
            print(prodect_key[0].items())
            for item in prodect_key:
                for key, value in item.items():
                    print("Checking key:", key)
                    if spotsymbol.upper() == key:
                        results.append({spot_symbol: key})
                        spot_symbol_detect.append(spot_symbol)
        check_2 = spot_symbol[:3]
        if not dex:
            if ".DE" in check_2:
                spotsymbol_2 = spot_symbol.split(".DE")[1]
                print(spotsymbol_2)
                for item in prodect_key:
                    for key, value in item.items():
                        if spotsymbol_2.upper() == key:
                            results.append({spot_symbol: key})
                            spot_symbol_detect.append(spot_symbol)


with open('dict_files\\spot_price.json', 'w') as f:
    json.dump(results, f)
