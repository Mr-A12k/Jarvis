import chromadb
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("jarvis_memory")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def add_documents(self, documents):
        for i, doc in enumerate(documents):
            embedding = self.model.encode(doc["content"]).tolist()
            self.collection.add(
                embeddings=[embedding],
                documents=[doc["content"]],
                ids=[str(i)]
            )

    def search(self, query, top_k=3):
        query_embedding = self.model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results["documents"][0]