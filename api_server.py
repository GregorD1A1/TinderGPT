from fastapi import FastAPI, Response
import uvicorn
import requests
from tnd_conn import DatingAppConnector
from typing import Dict

app = FastAPI()
tnd_connector = DatingAppConnector()

@app.get('/liking')
def like():
    open_tnd()
    liking_tnd(5)
    close_tnd()
    return {'responce': 'Liking function executed successfully!'}


@app.get('/get_msgs')
def get_messages():
    print("msgs request arrived")
    tnd_connector.open_tinder()
    messages = tnd_connector.get_msgs()
    requests.post('https://hook.eu1.make.com/esw5fwmyqwp2nxpyq51ii1k4abl2f65i',
                  json={'type': 'messages', 'content': messages})
    return 200


@app.get('/close')
def close_tnd():
    tnd_connector.close_tinder()
    return 200


@app.get('/get_bio')
def get_unwritten_girl_bio():
    print("bio request arrived")
    tnd_connector.open_tinder()
    name, bio = tnd_connector.get_first_match_bio()
    # send request to webhook
    requests.post('https://hook.eu1.make.com/esw5fwmyqwp2nxpyq51ii1k4abl2f65i', json={'type': 'bio', 'content': bio})
    return 200


@app.post("/send_message")
def send_message_endpoint(message: Dict[str, str]):
    print("message request arrived")
    tnd_connector.send_messages([message["message"]])
    return 200


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=80)
