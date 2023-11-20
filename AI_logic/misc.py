from dotenv import load_dotenv, find_dotenv
import os
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser


load_dotenv(find_dotenv())
language = os.environ['LANGUAGE']


def translate_rise_msg(message):
    prompt = ("Translate message to {language}, leave same style and emoticons. Message is directed to woman."
              "\n\nMessage: {message}")
    prompt = PromptTemplate.from_template(prompt)
    llm = ChatOpenAI(model='gpt-4-1106-preview', temperature=0.5)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({'message': message, 'language': language})