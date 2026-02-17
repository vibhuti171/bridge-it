import faiss
import numpy as np
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings


class SimpleVectorStore:
    def __init__(self):

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001", 
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

        test_vector = self.embeddings.embed_query("test")
        self.dimension = len(test_vector)

        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts = []

    def add_text(self, text: str):
        vector = self.embeddings.embed_query(text)
        vector_np = np.array([vector], dtype="float32")
        self.index.add(vector_np)
        self.texts.append(text)

    def search(self, query: str, k: int = 3):

        if len(self.texts) == 0:
            return []

        vector = self.embeddings.embed_query(query)
        vector_np = np.array([vector], dtype="float32")

        D, I = self.index.search(vector_np, min(k, len(self.texts)))

        return [self.texts[i] for i in I[0] if i < len(self.texts)]
