from extract import Extract
from embedding import Embedding
import numpy as np
import ast

def unpack(data):
    unpack = data[:, 4]
    res = [np.array(eval(sub_array)) for sub_array in unpack]
    return res


def main():
    extract = Extract()
    embedding = Embedding()
    data = extract.get_data_rss()
    data = extract.save_data(data)
    data = np.array(data)

    test_data = "Nagui"
    test_data = embedding.embedding(test_data)
    title_vectors = unpack(data)
    data_index = embedding.get_similar(test_data, title_vectors)

    print("title =", data[data_index[0]][0])
    print("title =", data[data_index[1]][0])
    print("title =", data[data_index[2]][0])

if __name__ == "__main__":
    main()