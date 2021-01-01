#!/usr/bin/python3

import requests
import json

url = 'http://localhost/broadcast'

body = {
    "command": "hello world",
    "broadcast": 1,
    "user": "saahil"
}

response = requests.post(url, json.dumps(body))

print(response)
