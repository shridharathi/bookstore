from sentence_transformers import SentenceTransformer
import numpy as np
import weaviate
import json

client = weaviate.Client('http://localhost:8080')

model = SentenceTransformer('thenlper/gte-base')

query_vector = model.encode("Find me a book about berlin")

result = client.query.get("Bookstore", ["title"]).with_near_vector({
    "vector": query_vector,
    "certainty": 0.7
}).with_limit(2).with_additional(['certainty', 'distance']).do()

print(json.dumps(result, indent=4))