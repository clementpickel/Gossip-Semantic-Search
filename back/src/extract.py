import feedparser
import csv
import re
import numpy as np
import pandas as pd
from src.database import Database

class Extract:
    np.set_printoptions(threshold=np.inf, suppress=True)

    rss_feeds = [
        "https://vsd.fr/actu-people/feed/",
        # "https://vsd.fr/tele/feed/",
        # "https://vsd.fr/societe/feed/",
        # "https://vsd.fr/culture/feed/",
        # "https://vsd.fr/loisirs/feed/",

        # "https://www.public.fr/feed",
        # "https://www.public.fr/people/feed",
        # "https://www.public.fr/tele/feed",
        # "https://www.public.fr/mode/feed",
        # "https://www.public.fr/people/familles-royales/feed",
    ]

    wanted_entries_key = [ # content should be here but it is a dict with more info so it is filterred in save_data
        "title",
        "link",
        "author",
    ]

    def __init__(self, db: Database):
        self.db = db
        pass

    def get_and_save(self):
        data = self.get_data_rss()
        self.db.wipe()
        self.save_data(data)

    def get_data_rss(self) -> list[dict]:
        data = []
        for feed in self.rss_feeds:
            d = feedparser.parse(feed)
            data.append(d)
            print("Got", feed)
        return data
    
    def save_data(self, datas):
        # Loading logic
        total_entries = sum(len(data["entries"]) for data in datas)
        processed_entries = 0
        progress_checkpoints = {i for i in range(10, 101, 10)}

        for data in datas:
            for entry in data["entries"]:
                content = self._remove_tags(entry["content"][0]["value"])
                title = self._remove_tags(entry["title"])
                self.db.add(title, entry["link"], entry["author"], content)
                
                # loading progress
                processed_entries += 1
                progress = int((processed_entries / total_entries) * 100)

                # loading display
                if int(progress) in progress_checkpoints:
                    print(f"Save entries to csv: {int(progress)}% completed")
                    progress_checkpoints.remove(int(progress))

    def _remove_tags(self, text):
        return re.sub(r"<.*?>", "", text.replace("\n", " "))
