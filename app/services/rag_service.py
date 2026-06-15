print("STEP 1")

from sentence_transformers import SentenceTransformer
import chromadb
from pypdf import PdfReader
print("STEP 2")

# model = SentenceTransformer("all-MiniLM-L6-v2")

model = None

def get_model():
    global model

    if model is None:
        print("Loading model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model

# conc to chromdb
client = chromadb.Client()
# storing  
collection = client.get_or_create_collection(name="policy_documents")
print("STEP 3")

def generate_text_embedding (text):
    model = get_model()
    return model.encode(text).tolist()
print("STEP 4")

def extract_text_from_pdf(pdf_path):

    reader= PdfReader(pdf_path)
    text=''

    for page in reader.pages:
        text+=page.extract_text()

    return text    

# to create chunk
def chunk_text(text,chunk_size=500):
    chunks=[]

    for  i in range(0,len(text),chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks    


# now to store chunk in chroma db

def store_policy_document(
    pdf_path
):

    text = extract_text_from_pdf(
        pdf_path
    )

    chunks = chunk_text(text)

    for index, chunk in enumerate(chunks):

        embedding = generate_text_embedding(
            chunk
        )

        collection.add(
            ids=[f"chunk_{index}"],
            documents=[chunk],
            embeddings=[embedding]
        )
    print(
        f"Stored {len(chunks)} chunks"
    )    
    print("TOTAL CHUNKS:", len(chunks))
    print("COLLECTION COUNT:", collection.count())


def search_policy_documents (question):

    embedding =generate_text_embedding(question)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )

    return results