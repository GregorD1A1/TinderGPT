import openai
import pinecone
import json


with open('api_keys.json', 'r') as f:
    api_keys = json.load(f)
openai.api_key = api_keys['openai']
MODEL = 'text-embedding-ada-002'
# init connection to pinecone
pinecone.init(api_keys['pinecone'], environment='asia-northeast1-gcp')
# connect to the index
index = pinecone.Index('textspl')

def query():
    query = 'Czas skupić się na zbudowaniu więzi emocjonalnej. W następnej wiadomości możesz spróbować zmienić temat rozmowy na coś bardziej osobistego i emocjonalnego, pytając ją o jakieś ważne dla niej wydarzenie lub doświadczenie z przeszłości (np. najpiękniejsze wspomnienie lub moment, który ją mocno wzruszył)'
    querry_embedding = openai.Embedding.create(input=query, engine=MODEL)['data'][0]['embedding']
    # querry responses
    response = index.query(queries=[querry_embedding], top_k=2, include_metadata=True)

    for match in response['results'][0]['matches']:
        print(match['metadata']['text'])
        print(match['score'])

index.delete(delete_all=True)