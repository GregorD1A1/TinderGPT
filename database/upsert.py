import openai
import pinecone
import json

with open('api_keys.json', 'r') as f:
    api_keys = json.load(f)
openai.api_key = api_keys['openai']
MODEL = 'text-embedding-ada-002'
# init connection to pinecone
#pinecone.init(api_keys['pinecone'], environment='asia-northeast1-gcp')
pinecone.init(api_keys['pinecone_en'], environment='us-west4-gcp-free')

# connect to the index
#index = pinecone.Index('textspl')
index = pinecone.Index('textseng')

#with open('baza_wiedzy.json', 'r', encoding='utf-8') as f:
with open('knowledge_base_eng.json', 'r', encoding='utf-8') as f:
    document = json.load(f)
    document = document['rules']

ids_document = [str(n) for n in range(len(document))]
# creates embeddings for the tags
response = openai.Embedding.create(
    input=[rule['tags'] for rule in document],
    engine=MODEL,
)
embeddings = [record['embedding'] for record in response['data']]

# prepare metadata
meta = [{'text': rule['text']} for rule in document]

# delete previous data
index.delete(delete_all=True)
# upsert data
upsert_data = zip(ids_document, embeddings, meta)
index.upsert(vectors=list(upsert_data))
print('Data been upserted to database')
