import requests, json


def test_example():
    url = "http://localhost:8000/v1/read/example"
    data = {"param1": "test_value"}
    response = requests.post(url, json=data).json()
    print(response)
    
    
if __name__ == "__main__":
    test_example()
    