import requests

payload = {
    "title": "Alan Turing",
    "text": "Alan Turing was an English mathematician, computer scientist, logician..."
}

response = requests.post("http://127.0.0.1:8000/generate_quiz", json=payload)

print("STATUS:", response.status_code)
print(response.text)
