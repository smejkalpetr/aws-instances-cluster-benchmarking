import requests
import time

# this is the client app that connects to the ELB and performs benchmarking
class Client:

    def run_requests(self, url, request_count1, request_count2, wait_time):
        headers = {'content_types': 'text/plain'}

        for i in range(request_count1):
            r = requests.get(url, headers=headers)
            body = r.content.decode("utf-8")

            print(f'{body}, Status code: {r.status_code}')

        if wait_time > 0:
            print(f"[CLIENT WAITING] The client is now waiting for {wait_time} seconds...")
            time.sleep(wait_time)

        for i in range(request_count2):
            r = requests.get(url, headers=headers)
            body = r.content.decode("utf-8")

            print(f'{body}, Status code: {r.status_code}')
