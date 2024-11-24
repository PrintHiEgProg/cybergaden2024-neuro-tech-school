import requests

url = "http://localhost:8000/api/auth/check/"
payload = {"username": "vlad", "password": "rootroot"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response Body:", response.text)
