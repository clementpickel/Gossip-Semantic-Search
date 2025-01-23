from transformers import CamembertModel, CamembertTokenizer
# import torch

class Embedding:
    tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
    camembert = CamembertModel.from_pretrained("camembert-base")

    def tokenize(self, text):
        return self.tokenizer.encode(text, add_special_tokens=True)

if __name__ == "__main__":
    emb = Embedding()
    print(emb.tokenize("Salut l'équipe"))
