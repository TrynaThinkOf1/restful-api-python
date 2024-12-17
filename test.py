import requests

url = "http://127.0.0.1:5000/user/"

#requests.post(f"{url}create", json={"email": "test@gmail.com", "passkey": "test_passkey"})
input()
print(requests.get(f"{url}email/test@gmail.com").content.decode('utf-8'))
input()