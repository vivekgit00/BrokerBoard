"""
Get Product_id
"""
# import requests
# import json
# responce = requests.get("https://api.delta.exchange/v2/products")
# data = responce.json()['result']
# # print(data.keys())
# results = []
# data_dict = {}
# for data in data:
#     print(str(data['id'])+ " " + data['symbol'])
#     results.append({data['symbol']: data['id']})
#
# with open('dict_files\\product_key.json', 'w') as f:
#     json.dump(results, f)


import threading
import time

# This Event object will be used to signal the thread to stop
stop_event = threading.Event()

# # Thread task
# def background_task(name):
#     print(f"[{name}] Started.")
#     # while not stop_event.is_set():
#     #     print(f"[{name}] Running...")
#     #     time.sleep(1)  # Simulate work
#     return  "ok"
#
# # Create the thread
# worker_thread = threading.Thread(target=background_task, args=("Worker-1",), daemon=True)
#
# # Start the thread
# print("Starting thread...")
# worker_thread.start()
#
# # Let it run for 5 seconds
# time.sleep(5)
#
# # Stop the thread using the event
# print("Stopping thread...")
# stop_event.set()
#
# # Wait for the thread to clean up
# worker_thread.join()
#
# # Check if thread is alive
# print("Thread is alive?", worker_thread.is_alive())
#
# print("Main thread done.")


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
