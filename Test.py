import requests

url = "https://api.freeapi.app/api/v1/kitchen-sink/http-methods/get"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.json())