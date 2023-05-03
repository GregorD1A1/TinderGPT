import openai
import pinecone


openai.api_key = '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'
MODEL = 'text-embedding-ada-002'
# init connection to pinecone
pinecone.init('82eefb80-b714-40d1-a91c-79968f96dd7e', environment='asia-northeast1-gcp')
# connect to the index
index = pinecone.Index('teksty')


query = 'How much legs have two dogs and one cat in common?'
querry_embedding = openai.Embedding.create(input=query, engine=MODEL)['data'][0]['embedding']
# querry responses
response = index.query(queries=[querry_embedding], top_k=2, include_metadata=True)

for match in response['results'][0]['matches']:
    print(match['metadata']['text'])
    print(match['score'])
