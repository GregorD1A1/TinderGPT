import os
import json
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from AI_logic.rule_base.rules_db_conn import query_rule
from AI_logic.airtable import get_record, upsert_record
from dotenv import load_dotenv, find_dotenv
from pushbullet import Pushbullet
from tenacity import retry, stop_after_attempt, wait_fixed

# api keys import
load_dotenv(find_dotenv())
language = os.environ['LANGUAGE']

current_dir = os.path.dirname(os.path.realpath(__file__))
# import prompt files
with open(f'{current_dir}/prompts/analyzer.prompt', 'r') as file:
    prompt_template = file.read()
analyzer_prompt = PromptTemplate.from_template(prompt_template)

with open(f'{current_dir}/prompts/commander_step1.prompt', 'r') as file:
    prompt_template = file.read()
commander_step1_prompt = PromptTemplate.from_template(prompt_template)

with open(f'{current_dir}/prompts/commander_step2.prompt', 'r') as file:
    prompt_template = file.read()
commander_step2_prompt = PromptTemplate.from_template(prompt_template)

with open(f'{current_dir}/prompts/writer.prompt', 'r') as file:
    prompt_template = file.read()
writer_prompt = PromptTemplate.from_template(prompt_template)

pushbullet_key = os.getenv('PUSHBULLET_API_KEY')
if pushbullet_key:
    pushbullet = Pushbullet(pushbullet_key)


Analyzer = ChatOpenAI(model='gpt-4', temperature=0)
Commander = ChatOpenAI(model='gpt-4', temperature=0.4)
Writer = ChatOpenAI(model='gpt-4', temperature=0.7)
#print(Writer.model_name)

analyser_chain = analyzer_prompt | Analyzer | StrOutputParser()
writer_chain = writer_prompt | Writer | StrOutputParser()


def commander_chain(future_step):
    if future_step == 'step1':
        return commander_step1_prompt | Commander | StrOutputParser()
    else:
        return commander_step2_prompt | Commander | StrOutputParser()


# retry decorator to retry if openai request didn't return
@retry(stop=stop_after_attempt(3), wait=wait_fixed(90))
def invoke_chain(chain, args, module_name=None):
    try:
        output = chain.invoke(args)
        output = json.loads(output)
        print(f'\n{module_name} says:')
        print(json.dumps(output, indent=4, ensure_ascii=False))
        return output
    except Exception as e:
        print(f"Error encountered: \n{str(e)}]n{str(e.args)}\nRetrying...")
        raise e


def respond_to_girl(name_age, messages):
    previous_summary = get_record(name_age)
    analyzer_output = invoke_chain(
        analyser_chain, {'summary': previous_summary, 'messages': messages}, 'Analyzer'
    )

    future_step = analyzer_output['future_step']
    summary = analyzer_output['summary']
    contact = analyzer_output['contact']
    if contact:
        pushbullet.push_note(f"I planned date with {name_age}", contact)
        return

    commander_output = invoke_chain(
        commander_chain(future_step), {'summary': summary, 'messages': messages},'Commander'
    )

    tags = commander_output['tags']
    rules = "\n###\n- ".join([query_rule(tag) for tag in tags])
    writer_output = invoke_chain(writer_chain, {
        'rules': rules,
        'messages': messages,
        'language': language,
    }, 'Writer')

    message = writer_output['message']
    # update summary in case of attractive guy image or storytelling
    if 'Attractive guy image' in tags or 'Storytelling' in tags:
        analyzer2_output = invoke_chain(
            analyser_chain, {'summary': summary, 'messages': f'Conversator: {message}'}, 'Analyzer2'
        )
        summary = analyzer2_output['summary']

    upsert_record(name_age, summary)
    return message
