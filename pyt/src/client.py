import json
import requests
import time
class Client:
    
    def get_request(self,url):
        headers={'content_types':'application/json'}
        r=requests.get(url,headers=headers)
        print(r.status_code)
        print(r.content)

    def run_requests(self,url):
        N=1000
        for i  in range(N):
            self.get_request(url)
        time.sleep(30)
        for i in range(N):
            self.get_request(url)

