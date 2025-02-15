import feedparser
import csv
import re
from src.embedding import Embedding
import numpy as np
import pandas as pd

class Extract:
    np.set_printoptions(threshold=np.inf, suppress=True)
    emb = Embedding()

    rss_feeds = [
        "https://vsd.fr/actu-people/feed/",
        "https://vsd.fr/tele/feed/",
        "https://vsd.fr/societe/feed/",
        "https://vsd.fr/culture/feed/",
        "https://vsd.fr/loisirs/feed/",

        "https://www.public.fr/feed",
        "https://www.public.fr/people/feed",
        "https://www.public.fr/tele/feed",
        "https://www.public.fr/mode/feed",
        "https://www.public.fr/people/familles-royales/feed",
    ]

    wanted_entries_key = [ # content should be here but it is a dict with useless info so it is filterred in save_data
        "title",
        "link",
        "author",
    ]

    def __init__(self):
        pass

    def get_data_rss(self) -> list[dict]:
        data = []
        for feed in self.rss_feeds:
            d = feedparser.parse(feed)
            data.append(d)
            print("Got", feed)
        return data
    
    def get_data_csv(self):
        data = pd.read_csv("articles.csv").to_numpy()
        return data
    
    def save_data(self, datas):
        res = []
        past_titles = []
        with open("articles.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(self.wanted_entries_key + ["content", "title_vector"])

            # Loading logic
            total_entries = sum(len(data["entries"]) for data in datas)
            processed_entries = 0
            progress_checkpoints = {i for i in range(10, 101, 10)}

            for data in datas:
                for entry in data["entries"]:
                    if entry["title"] not in past_titles:
                        past_titles.append(entry["title"])
                        title_vector = self.emb.embedding(entry["title"])
                        content = self._remove_tags(entry["content"][0]["value"])

                        line = [entry[key] for key in self.wanted_entries_key] + [content, np.array2string(title_vector, separator=',').replace("\n", "")]

                        writer.writerow(line)
                        res.append(line)
                        
                        # loading progress
                        processed_entries += 1
                        progress = int((processed_entries / total_entries) * 100)

                        # loading display
                        if int(progress) in progress_checkpoints:
                            print(f"Save entries to csv: {int(progress)}% completed")
                            progress_checkpoints.remove(int(progress))
        return res

    def _remove_tags(self, text):
        return re.sub(r"<.*?>", "", text.replace("\n", " "))
    
    def unpack(self, data):
        unpack = data[:, 4]
        res = [np.array(eval(sub_array)) for sub_array in unpack]
        return res
    
    def line_to_json(self, line):
        return {
            "title": line[0],
            "link": line[1],
            "author": line[2],
            "content": line[3],
        }