import requests
import time
import random


def session():
    requests.get('http://localhost:8080/open_app')
    requests.get('http://localhost:8080/get_msgs')
    time.sleep(random.uniform(90, 120))
    requests.get('http://localhost:8080/get_msgs')
    time.sleep(random.uniform(90, 120))
    requests.get('http://localhost:8080/get_msgs')
    time.sleep(random.uniform(90, 120))
    requests.get('http://localhost:8080/get_bio')
    time.sleep(random.uniform(30, 60))
    requests.get('http://localhost:8080/close')

if __name__ == '__main__':
    session()