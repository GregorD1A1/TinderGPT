import openai
import pinecone


openai.api_key = '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'
MODEL = 'text-embedding-ada-002'
# init connection to pinecone
pinecone.init('82eefb80-b714-40d1-a91c-79968f96dd7e', environment='asia-northeast1-gcp')
# connect to the index
index = pinecone.Index('teksty')


document = ['cats have two legs', 'dogs have three legs', 'cats are smarter than dogs', 'penguins are smarter than cats']
ids_document = [str(n) for n in range(len(document))]
# creates embeddings for the given text
response = openai.Embedding.create(
    input = document,
    engine=MODEL,
)

embeddings = [record['embedding'] for record in response['data']]

# prepare metadata
meta = [{'text': text} for text in document]
# upsert data
upsert_data = zip(ids_document, embeddings, meta)
index.upsert(vectors=list(upsert_data))

