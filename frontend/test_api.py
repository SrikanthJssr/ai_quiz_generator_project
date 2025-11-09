import requests, json

API = "http://127.0.0.1:8000"

def test_extract():
    r = requests.get(f"{API}/extract", params={"url":"https://en.wikipedia.org/wiki/Alan_Turing"})
    print("STATUS", r.status_code)
    try:
        print(json.dumps(r.json(), indent=2))
    except:
        print(r.text)

def test_generate():
    r = requests.post(f"{API}/generate_quiz", json={"url":"https://en.wikipedia.org/wiki/Alan_Turing"})
    print("STATUS", r.status_code)
    try:
        print(json.dumps(r.json(), indent=2))
    except:
        print(r.text)

if __name__ == "__main__":
    test_extract()
    print("-----")
    test_generate()
