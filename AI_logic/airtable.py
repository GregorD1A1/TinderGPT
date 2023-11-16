import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

token = os.environ['AIRTABLE_TOKEN']
workspace_id = os.environ['AIRTABLE_WORKSPACE_ID']
base_id = os.getenv('AIRTABLE_BASE_ID')
table_id = os.getenv('AIRTABLE_TABLE_ID')

url_bases = "https://api.airtable.com/v0/meta/bases"
auth_header = {
  "Authorization": f"Bearer {token}",
  "Content-Type": "application/json"
}


def create_base():
    data = {
      "name": "TinderGPT",
      "tables": [
        {
          "description": "Data about your current conversations",
          "fields": [
            {
              "name": "name_age",
              "type": "singleLineText"
            },
            {
              "name": "summary",
              "type": "singleLineText",
              "description": "summary of previous conversation"
            },
            {
              "name": "last_contact",
              "type": "singleLineText"
            },
          ],
          "name": "Girls summaries"
        }
      ],
      "workspaceId": workspace_id,
    }

    response = requests.post(url_bases, headers=auth_header, data=json.dumps(data))
    base_id = response.json()['id']
    table_id = response.json()['tables'][0]['id']

    return base_id, table_id


def get_record(name_age):
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
    response = requests.get(url, headers=auth_header)
    records = response.json()['records']
    record = next((record['fields'] for record in records if record['fields'].get('name_age') == name_age), None)
    return record["summary"] if record else None


def upsert_record(name_age, summary):
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
    data = {
        "performUpsert": {
            "fieldsToMergeOn": [
                "name_age"
            ]
        },
        "records": [
            {
                "fields": {
                    "name_age": name_age,
                    "summary": summary,
                    "last_contact":  datetime.today().strftime('%d-%m-%Y')
                },
            }
        ]
    }
    requests.patch(url, headers=auth_header, data=json.dumps(data))


def girls_to_rise():
    # start date 3 days ago
    start_date = datetime.today() - timedelta(days=2)
    # end date 9 days ago
    end_date = datetime.today() - timedelta(days=10)
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
    all_girls = requests.get(url, headers=auth_header)
    girls_to_rise = []
    for record in all_girls.json()['records']:
        date_of_record = datetime.strptime(record['fields']['last_contact'], '%d-%m-%Y')
        if start_date > date_of_record > end_date:
            # append name_age to list
            girls_to_rise.append(record['fields']['name_age'])

    return girls_to_rise




# create new base if no base saved in .env file
if not base_id:
    base_id, table_id = create_base()
    with open(".env", "a") as env_file:
        env_file.write(f"\nAIRTABLE_BASE_ID={base_id}\n")
        env_file.write(f"AIRTABLE_TABLE_ID={table_id}\n")
