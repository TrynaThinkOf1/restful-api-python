import requests

requests.post(f"http://127.0.0.1:5000/user/{input('Enter email: ')}", {"passkey": input('Enter passkey: ')})

print(requests.get(f"http://127.0.0.1:5000/user/{input('Enter email: ')}"))