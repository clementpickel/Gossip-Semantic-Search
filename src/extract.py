import feedparser
import csv
import re
from embedding import Embedding
import numpy as np

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
        return data
    
    def get_data_csv(self):
        pass
    
    def save_data(self, datas):
        res = []
        with open("articles.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(self.wanted_entries_key + ["content", "title_vector"])

            for data in datas:
                for entry in data["entries"]:
                    title_vector = self.emb.embedding(entry["title"])
                    content = self._remove_tags(entry["content"][0]["value"])

                    line = [entry[key] for key in self.wanted_entries_key] + [content, np.array2string(title_vector, separator=',').replace("\n", "")]

                    writer.writerow(line)
                    res.append(line)
        return res

    def _remove_tags(self, text):
        return re.sub(r"<.*?>", "", text.replace("\n", " "))
