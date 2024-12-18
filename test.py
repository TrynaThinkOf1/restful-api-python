import requests

url = "http://127.0.0.1:6969"

def post():
    post = requests.post(f"{url}/user", json={"email": input("Email: "), "passkey": input("Passkey: ")})
    print(post.content.decode())
    print(requests.get(f"{url}/user/{input("Email: ")}").content.decode('utf-8'))

post()