from fastapi import FastAPI, Response
import uvicorn
import requests
from tnd_conn import DatingAppConnector
from typing import Dict

app = FastAPI()
tnd_connector = DatingAppConnector()


@app.get('/')
def check_driver_state():
    response = "Driver up and running" if tnd_connector.driver else "Driver not running"
    return response


@app.get('/get_msgs')
def get_newest_messages():
    print("msgs request arrived")
    messages = tnd_connector.get_msgs()
    requests.post('https://hook.eu1.make.com/esw5fwmyqwp2nxpyq51ii1k4abl2f65i',
                  json={'type': 'messages', 'content': messages})
    return 200


@app.get('/get_msgs/{girl_nr}')
def get_messages_with_nr(girl_nr: int = None):
    print("msgs request arrived")
    messages = tnd_connector.get_msgs(girl_nr)
    requests.post('https://hook.eu1.make.com/esw5fwmyqwp2nxpyq51ii1k4abl2f65i',
                  json={'type': 'messages', 'content': messages})
    return 200


@app.get('/get_bio')
def get_unwritten_girl_bio():
    print("bio request arrived")
    name, bio = tnd_connector.get_first_match_bio()
    # send request to webhook
    print('sending request to webhook')
    requests.post('https://hook.eu1.make.com/esw5fwmyqwp2nxpyq51ii1k4abl2f65i', json={'type': 'bio', 'content': bio})
    return 200


@app.post("/send_message")
def send_message_endpoint(message: Dict[str, str]):
    print("message request arrived")
    tnd_connector.send_messages([message["message"]])
    return 200


if __name__ == '__main__':
    print("Opening Tinder")
    tnd_connector.open_tinder()
    print("Tinder activated")
    uvicorn.run(app, host='127.0.0.1', port=8080)
