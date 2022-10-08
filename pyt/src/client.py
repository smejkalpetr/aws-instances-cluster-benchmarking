import json
import requests
import time
def get_request(url):
    headers={'content_types':'application/json'}
    r=requests.get(url,headers=headers)
    print(r.status_code)
    print(r.json())

def run_requests(url):
    N=1000
    for i  in range(N):
        get_request(url)
    time.sleep(30)
    for i in range(N):
        get_request(url)

