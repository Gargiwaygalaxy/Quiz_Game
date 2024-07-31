import requests

parameters = {
    "amount": 10,
    "type": "multiple"
}

response = requests.get(url="https://opentdb.com/api.php?amount=10&category=18&difficulty=medium&type=multiple", params=parameters)
question_data = response.json()["results"]
