import chromadb
import numpy as np


client = chromadb.Client()

collection =client.get_or_create_collection(
    name ="claim_embeddings"
)

def store_claim_embeddings(claim_id , embedding):

    embedding = np.array(
        embedding
    ).flatten().tolist()

    print("TYPE:", type(embedding))
    print("LEN:", len(embedding))
    print("FIRST:", type(embedding[0]))
    print("SAMPLE:", embedding[:3])

    collection.add(
        ids=[str(claim_id)],
        embeddings=[embedding]
    )



def search_similar_claims(embedding):
    count = collection.count()
    if count ==0:
        return None

    embedding = np.array(
        embedding
    ).flatten().tolist()

    results=collection.query(
        query_embeddings=[embedding],
        n_results= min(3,count)
    )    


    return results