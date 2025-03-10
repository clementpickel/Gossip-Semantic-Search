import faiss
import numpy as np
import google.generativeai as genai
from src.dto import DBElem
import pickle
from src.env import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

class Database:

    def __init__(self, vector_dim=768):
        """Initialize the database with an FAISS index and a metadata storage."""
        self.vector_dim = vector_dim
        self.index = faiss.IndexFlatL2(vector_dim)
        self.metadata = []

    def get_emb(self, content):
        response = genai.embed_content(
            model="models/embedding-001",
            content=content, 
            task_type="retrieval_document"
        )

        if "embedding" not in response:
            raise ValueError("Embedding generation failed")

        vector = np.array(response["embedding"], dtype="float32")
        return vector
    
    def add(self, title, link, author, content):
        """Generate an embedding using Gemini and add the entry to the database."""
        vector = self.get_emb(title)

        if vector.shape[0] != self.vector_dim:
            raise ValueError(f"Expected vector of size {self.vector_dim}, got {vector.shape[0]}")

        self.index.add(vector.reshape(1, -1))
        self.metadata.append(DBElem(title=title, link=link, author=author, content=content, vector=vector))
    
    def get_similar(self, query_vector, k=3):
        if len(query_vector) != self.vector_dim:
            raise ValueError(f"Query vector must have dimension {self.vector_dim}, but got {len(query_vector)}")

        query_vector = np.array([query_vector], dtype="float32")
        distances, indices = self.index.search(query_vector, k)
        print("distance=", distances)
        print("indice=", indices)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                entry = self.metadata[idx]
                results.append({
                    "title": entry.title,
                    "link": entry.link,
                    "author": entry.author,
                    "content": entry.content,
                    "distance": float(distances[0][i])
                })

        return results
    
    def save(self, path):
        """Save the database to a file."""
        faiss.write_index(self.index, path + ".index")
        with open(path + ".meta", "wb") as f:
            pickle.dump(self.metadata, f)
    
    def load(self, path):
        """Load the database from a file."""
        self.index = faiss.read_index(path + ".index")
        with open(path + ".meta", "rb") as f:
            self.metadata = pickle.load(f)

    def wipe(self):
        """Wipe the database by reinitializing the FAISS index and clearing metadata."""
        self.index = faiss.IndexFlatL2(self.vector_dim)
        self.metadata.clear()

    def print(self):
        for data in self.metadata:
            print(data)




if __name__ == "__main__":
    db = Database()
    # db.load("db")
    test_article: list[DBElem] = [
    DBElem(
        title="David Pujadas le bg de l'info",
        content="article intéressant",
        link="http://google.com",
        author="moi oim",
    ),
    DBElem(
        title="La reine d'Angleterre ressuscitée 3 jours après",
        content="article intéressant",
        link="http://google.com",
        author="moi oim",
    ),
    DBElem(
        title="Linkup: l'endroit idéal pour faire un stage ?",
        content="article intéressant",
        link="http://google.com",
        author="moi oim",
    )
    ]

    for article in test_article:
        db.add(article.title, article.link, article.author, article.content)

    vector = db.get_emb('La princesse diana passe par dessus la troisième corde')

    res = db.get_similar(vector, 1)
    for article in res:
        print(article)
    db.save('test')
    db.load('test')
