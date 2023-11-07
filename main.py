from fastapi import FastAPI, Response
import uvicorn
import argparse
from typing import Dict
from connectors.tnd_conn import TinderConnector
from connectors.bdo_conn import BadooConnector
from connectors.bmb_conn import BumbleConnector
from driver.driver import start_driver
import AI_logic.respond
import AI_logic.opener
from dotenv import load_dotenv, find_dotenv
from importlib import reload


load_dotenv(find_dotenv())
app = FastAPI()
parser = argparse.ArgumentParser()
parser.add_argument('-he', '--head', action='store_true',
                    help='selenium in head (non-headless) option')
args = parser.parse_args()


@app.get('/')
def check_driver_state():
    response = "Driver up and running" if dating_connector.driver else "Driver not running"
    return response


@app.get('/start_tnd')
def load_main_page_tnd():
    print("main page request arrived")
    global dating_connector
    dating_connector = tinder_connector
    dating_connector.load_main_page()
    return 200


@app.get('/start_bdo')
def load_main_page_bdo():
    print("main page request arrived")
    global dating_connector
    dating_connector = badoo_connector
    dating_connector.load_main_page()
    return 200


@app.get('/start_bmb')
def load_main_page_bmb():
    print("main page request arrived")
    global dating_connector
    dating_connector = bumble_connector
    dating_connector.load_main_page()
    return 200


@app.get('/respond')
def get_newest_messages():
    print("msgs request arrived")
    messages = dating_connector.get_msgs()
    name_age = dating_connector.get_name_age()
    response = AI_logic.respond.respond_to_girl(name_age, messages)
    send_message_endpoint({'message': response})
    return 200


@app.get('/respond/{girl_nr}')
def get_messages_with_nr(girl_nr: int = None):
    print("msgs request arrived")
    messages = dating_connector.get_msgs(girl_nr)
    name_age = dating_connector.get_name_age()
    response =  dating_connector.get_name_age()
    response = AI_logic.respond.respond_to_girl(name_age, messages)
    send_message_endpoint(payload={'message': response})
    return 200


@app.get('/opener')
def get_unwritten_girl_bio():
    print("bio request arrived")
    name, bio = dating_connector.get_bio()
    message = AI_logic.opener.generate_opener(name, bio)
    send_message_endpoint({'message': message})
    return 200


@app.get('/opener/{girl_nr}')
def get_unwritten_girl_bio(girl_nr: int = None):
    print("bio request arrived")
    name, bio = dating_connector.get_bio(girl_nr)
    message = AI_logic.opener.generate_opener(name, bio)
    send_message_endpoint({'message': message})
    return 200


@app.post("/send_message")
def send_message_endpoint(payload: Dict[str, str]):
    print("message request arrived")
    dating_connector.send_message(payload['message'])
    return 200

@app.get("/close")
def close_app():
    dating_connector.close_app()
    return 200

# use that endpoint to reload AI modules after providing changes on propmts or AI modules code
# without restarting whole application
@app.get('/reload')
async def reload_modules():
    reload(AI_logic.respond)
    reload(AI_logic.opener)

    return {"message": "Modules reloaded"}


if __name__ == '__main__':
    driver = start_driver(args.head)
    tinder_connector = TinderConnector(driver)
    #badoo_connector = BadooConnector(driver)
    #bumble_connector = BumbleConnector(driver)
    dating_connector = tinder_connector
    uvicorn.run(app, host='127.0.0.1', port=8080)
