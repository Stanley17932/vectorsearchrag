import pymongo
from openai import OpenAI

client = OpenAI(api_key="<open_ai_api_key>")

#set your openai API key

client = pymongo.MongoClient("XXXXXXX")
db = client.sample_mflix
collection = db.embedded_movies


def generate_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
        )

    return response.data[0].embedding


query ="imaginary characters from outer space at war"

results = collection.aggregate([
    {"$vectorSearch": {
        "queryVector": generate_embedding(query), 
        "path": "plot_embedding",
        "numCandidates":100,
        "limit":4,
        "index":"PlotSemanticSearch",
    }}
])

for document in results:
    print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')