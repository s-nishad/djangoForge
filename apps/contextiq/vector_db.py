import os
import uuid
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)



# ----------------------------
# Minimal Document class
# ----------------------------
class SimpleDocument:
    def __init__(self, page_content: str, metadata: dict = None):
        self.page_content = page_content
        self.metadata = metadata or {}
        self.id = str(uuid.uuid4())  # unique ID for Chroma compatibility

# ----------------------------
# Vector DB initialization
# ----------------------------
VECTOR_DB_PATH = "db/chroma_docs"
os.makedirs(VECTOR_DB_PATH, exist_ok=True)

# Use a local HuggingFace model for embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize Chroma vector database
vector_db = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embeddings, collection_name="documents")

# ----------------------------
# Save content to vector DB
# ----------------------------
def save_to_vector_db(content: str, metadata: dict):
    """Save parsed text to Chroma vector database."""
    if not content:
        raise ValueError("No content to save to vector database.")

    # Split document into semantically meaningful chunks
    chunks = text_splitter.split_text(content)
    docs = [SimpleDocument(page_content=chunk, metadata=metadata) for chunk in chunks]
    vector_db.add_documents(docs)
    vector_db.persist()

# ----------------------------
# Query vector DB
# ----------------------------
def query_vector_db(query: str, top_k: int = 3):
    """
    Retrieve top matching documents from vector database.

    Args:
        query (str): The search query.
        top_k (int): Number of top results to return.

    Returns:
        List[SimpleDocument]: List of matching documents.
    """
    if not query:
        raise ValueError("Query cannot be empty.")
    
    results = vector_db.similarity_search(query, k=top_k)
    return results
