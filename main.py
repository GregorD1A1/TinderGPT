from fastapi import FastAPI, Response
import uvicorn
import argparse
from typing import Dict
from driver.connectors.tnd_conn import TinderConnector
from driver.driver import start_driver
import AI_logic.respond
import AI_logic.opener
import AI_logic.airtable
from dotenv import load_dotenv, find_dotenv
from importlib import reload
import os


load_dotenv(find_dotenv())
use_tindebielik = os.getenv('USE_TINDEBIELIK')

if use_tindebielik:
    import AI_logic.respond_tindebielik

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



@app.get('/respond/{girl_nr}')
def respond_nr(girl_nr: int = None):
    print("msgs request arrived")
    messages = dating_connector.get_msgs(girl_nr)
    name_age = dating_connector.get_name_age()
    if not use_tindebielik:
        response = AI_logic.respond.respond_to_girl(name_age, messages)
    else:
        response = AI_logic.respond_tindebielik.respond_to_girl_tindebielik(name_age, messages)
    send_messages_endpoint(payload={'message': response})
    return 200


@app.get('/respond')
def respond():
    return respond_nr()

@app.get('/respond_all')
def respond_to_all():
    print("respond all request arrived")
    new_messages_nr = dating_connector.count_new_messages()
    for i in range(new_messages_nr):
        respond()

    return 200


@app.get('/opener')
def write_opener():
    print("opener request arrived")
    name, bio = dating_connector.get_bio()
    message = AI_logic.opener.generate_opener(name, bio)
    send_messages_endpoint({'message': message})
    return 200


# function to send predefined nr of openers
@app.get('/batch_openers/{nr_openers}')
def write_openers(nr_openers: int = None):
    print("batch of openers request arrived")
    for i in range(nr_openers):
        name, bio = dating_connector.get_bio()
        message = AI_logic.opener.generate_opener(name, bio)
        send_messages_endpoint({'message': message})
    return 200


@app.get('/opener/{girl_nr}')
def write_opener(girl_nr: int = None):
    print("opener request arrived")
    name, bio = dating_connector.get_bio(girl_nr)
    message = AI_logic.opener.generate_opener(name, bio)
    send_messages_endpoint({'message': message})
    return 200


@app.get('/rise')
def rise_girls():
    print("Rise request arrived")
    dating_connector.rise_girls()
    return 200


@app.get('/clear_base')
def remove_expired():
    print("Clear base request arrived")
    AI_logic.airtable.remove_expired_girls()
    return 200


@app.post("/send_message")
def send_messages_endpoint(payload: Dict[str, str]):
    print("message request arrived")
    dating_connector.send_messages(payload['message'])
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
    reload(AI_logic.airtable)

    return {"message": "Modules reloaded"}


if __name__ == '__main__':
    driver = start_driver(args.head)
    tinder_connector = TinderConnector(driver)
    #badoo_connector = BadooConnector(driver)
    #bumble_connector = BumbleConnector(driver)
    dating_connector = tinder_connector
    uvicorn.run(app, host='127.0.0.1', port=8080)
