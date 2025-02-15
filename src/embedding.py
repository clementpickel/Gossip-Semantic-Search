from transformers import CamembertModel, CamembertTokenizer
import numpy as np

class Embedding:
    tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
    camembert = CamembertModel.from_pretrained("camembert-base")

    def embedding(self, text):
        tokenized_sentence = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        embeddings = self.camembert(**tokenized_sentence)
        return embeddings["last_hidden_state"].mean(dim=1).detach().numpy().squeeze()
    
    def get_similar(self, test_vector, article_vectors):
        similarity = [np.dot(test_vector, article_vector) / (np.linalg.norm(test_vector) * np.linalg.norm(article_vector)) for article_vector in article_vectors]
        sorted_indices = sorted(range(len(similarity)), key=lambda i: similarity[i], reverse=True)
        return sorted_indices

if __name__ == "__main__":
    emb = Embedding()
    test_article_title = ["David Pujadas le bg de l'info", "La reine d'angleterre résucité 3 jours après", "Linkup: l'endroit idéale pour faire un stage ?"]
    test_article_title_vector = [emb.embedding(title) for title in test_article_title]
    test_title = emb.embedding("Royaume Unis")

    index = emb.get_similar(test_title, test_article_title_vector)
    print("title =", test_article_title[index[0]])
    print("title =", test_article_title[index[1]])
    print("title =", test_article_title[index[2]])
