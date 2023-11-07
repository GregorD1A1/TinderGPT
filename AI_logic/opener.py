import os
import json
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from tenacity import retry, stop_after_attempt, wait_fixed
from dotenv import load_dotenv, find_dotenv


# API keys import
load_dotenv(find_dotenv())
language = os.environ['LANGUAGE']

current_dir = os.path.dirname(os.path.realpath(__file__))
with open(f'{current_dir}/prompts/opener.prompt', 'r') as file:
    prompt_template = file.read()

prompt = PromptTemplate.from_template(prompt_template)

llm = ChatOpenAI(model='gpt-4', temperature=0.8)

chain = prompt | llm | StrOutputParser()

def log_retry(retry_state):
    print("Did not received response from OpenAI. Retrying request...")


@retry(stop=stop_after_attempt(3), wait=wait_fixed(90), before_sleep=log_retry)
def generate_opener(name, description):
    return chain.invoke({'name': name, 'description': description, 'language': language})
