import requests
import time
import random


def session():
    requests.get('http://localhost:8080/open_tnd')
    requests.get('http://localhost:8080/get_msgs')
    time.sleep(random.uniform(45, 70))
    requests.get('http://localhost:8080/get_msgs')
    time.sleep(random.uniform(45, 70))
    requests.get('http://localhost:8080/get_bio')
    time.sleep(random.uniform(10, 30))
    requests.get('http://localhost:8080/close')

if __name__ == '__main__':
    session()