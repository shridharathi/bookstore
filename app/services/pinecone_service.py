#import pinecone as pc
from pinecone import Pinecone, PodSpec
from app.services.openai_service import get_embedding
import os

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

# make sure to enter your actual Pinecone environment

pc = Pinecone(api_key=PINECONE_API_KEY, environment='gcp-starter')
#pc.init(api_key=PINECONE_API_KEY, environment='gcp-starter')

EMBEDDING_DIMENSION = 768

def delete_index():
   for index in pc.list_indexes():
      pc.delete_index(name=index['name'])

def embed_chunks_and_upload_to_pinecone(books, embeds, index_name):

    # delete the index if it already exists. 
    # as Pinecone's free plan only allows one index
    for index in pc.list_indexes():
        pc.delete_index(name=index['name'])
    # create a new index in Pinecone
    # the EMBEDDING_DIMENSION is based on what the
    # OpenAI embedding model outputs
    pc.create_index(name=index_name,
                    dimension=EMBEDDING_DIMENSION, 
                    metric='cosine',
                    spec=PodSpec(
                        environment="gcp-starter"
                    ))
    index = pc.Index(index_name)
    # embed each chunk and aggregate these embeddings
    embeddings_with_ids = []
    for i, row in books.iterrows():
        metadata ={"title": row["Title"],
                   "author": row["Authors"],
                   "category": row["Category"],
                   "description": row["Description"],
                   "price": row["Price Starting With ($)"]}
        embeddings_with_ids.append((str(i), embeds[i], metadata))
        if i % 500 == 0:
            print(i)
            # upload the embeddings and relevant texts for each chunk
            # to the Pinecone index
            upserts = [(id, vec, metadata) for id, vec, metadata in embeddings_with_ids]
            index.upsert(vectors=upserts)
            embeddings_with_ids = []


def get_most_similar_chunks_for_query(query, index_name):
    question_embedding = get_embedding(query)
    index = pc.Index(index_name)
    query_results = index.query(vector=question_embedding, top_k=2, include_metadata=True)
    def get_metadata(result):
        return str({"title": result["title"],
                "author": result["author"],
                "category": result["category"],
                "description": result["description"],
                "price": result["price"]})
    context =  "Book 1: " + get_metadata(query_results['matches'][0]['metadata'])+ "; Book 2: " + get_metadata(query_results['matches'][0]['metadata'])
    return context
