from fastapi import FastAPI, Response
import uvicorn
import requests
from typing import Dict
from connectors.tnd_conn import TinderConnector
from connectors.bdo_conn import BadooConnector
from connectors.bmb_conn import BumbleConnector
from driver.driver import start_driver

#MAKE_HOOK = 'https://hook.eu1.make.com/esw5fwmyqwp2nxpyq51ii1k4abl2f65i'
MAKE_HOOK = 'https://hook.eu1.make.com/9d2aig2r01r2jvqljx84jf66yoev28zh'
app = FastAPI()


@app.get('/')
def check_driver_state():
    response = "Driver up and running" if dating_connector.driver else "Driver not running"
    return response

@app.get('/open_tnd')
def load_main_page_tnd():
    print("main page request arrived")
    global dating_connector
    dating_connector = tinder_connector
    dating_connector.load_main_page()
    return 200

@app.get('/open_bdo')
def load_main_page_bdo():
    print("main page request arrived")
    global dating_connector
    dating_connector = badoo_connector
    dating_connector.load_main_page()
    return 200

@app.get('/open_bmb')
def load_main_page_bmb():
    print("main page request arrived")
    global dating_connector
    dating_connector = bumble_connector
    dating_connector.load_main_page()
    return 200


@app.get('/get_msgs')
def get_newest_messages():
    print("msgs request arrived")
    messages = dating_connector.get_msgs()
    name_age = dating_connector.get_name_age()
    requests.post(MAKE_HOOK, json={'type': 'messages', 'content': messages, 'name_age': name_age})
    return 200


@app.get('/get_msgs/{girl_nr}')
def get_messages_with_nr(girl_nr: int = None):
    print("msgs request arrived")
    messages = dating_connector.get_msgs(girl_nr)
    name_age = dating_connector.get_name_age()
    requests.post(MAKE_HOOK, json={'type': 'messages', 'content': messages, 'name_age': name_age})
    return 200


@app.get('/get_bio')
def get_unwritten_girl_bio():
    print("bio request arrived")
    name, bio = dating_connector.get_bio()
    # send request to webhook
    print('sending request to webhook')
    requests.post(MAKE_HOOK, json={'type': 'bio', 'content': bio, 'name_age': name})
    return 200


@app.get('/get_bio/{girl_nr}')
def get_unwritten_girl_bio(girl_nr: int = None):
    print("bio request arrived")
    name, bio = dating_connector.get_bio(girl_nr)
    # send request to webhook
    print('sending request to webhook')
    requests.post(MAKE_HOOK, json={'type': 'bio', 'content': bio, 'name_age': name})
    return 200


@app.post("/send_message")
def send_message_endpoint(payload: Dict[str, str]):
    print("message request arrived")
    dating_connector.send_message(payload['message'], payload['girl_type'])
    return 200

@app.get("/close")
def close_app():
    dating_connector.close_app()
    return 200


if __name__ == '__main__':
    driver = start_driver()
    tinder_connector = TinderConnector(driver)
    badoo_connector = BadooConnector(driver)
    bumble_connector = BumbleConnector(driver)
    uvicorn.run(app, host='127.0.0.1', port=8080)
