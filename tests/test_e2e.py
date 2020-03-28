import json
import requests
import os


def test_api_works():
    url = os.getenv("EMAIL_LAMBDA_URL")
    body = {"to": "cassie_tutoring", "message": "This is the message", "email": "test@gmail.com", "name": "test test"}
    r = requests.post(url=url, data=json.dumps(body))
    assert r.status_code < 299
    print(r.status_code)
