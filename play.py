#!/usr/bin/python3

import requests
import json

url = 'http://192.168.0.2:3000/assistant'

body = {
    "command": "Prayer Time!",
    "broadcast": 1,
    "user": "saahil" 
}

response = requests.post(url, body)

print(response)
