import json
import requests
def get_request(url):
    headers={'content_types':'application/json'}
    r=requests.get(url,headers=headers)
    print(r.status_code)
    print(r.json())

