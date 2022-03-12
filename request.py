import requests
import json


url = "http://127.0.0.1:5000/post/"

requests.post(
    url, json.dumps({"clef": "python"}), headers={"Content-Type": "application/json"}
)
