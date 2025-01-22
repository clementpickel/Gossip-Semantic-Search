import feedparser
import csv

class Extract:
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
        write_header = True
        with open("articles.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for data in datas:
                for entry in data["entries"]:
                    if write_header:
                        write_header = False
                        writer.writerow(entry.keys())
                    writer.writerow([entry[key] for key in entry.keys()])