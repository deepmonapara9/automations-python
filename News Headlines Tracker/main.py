import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

RSS_FEEDS = [
    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "https://www.indiatoday.in/rss/home",
    "https://feeds.feedburner.com/ndtvnews-top-stories",
    "https://www.hindustantimes.com/feeds/rss/topnews/rssfeed.xml",
]


def log_headlines():
    while True:
        with open("news_log.txt", "a", encoding="utf-8") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"\n🕒 {timestamp}\n")

            for feed in RSS_FEEDS:
                try:
                    r = requests.get(feed, timeout=10)
                    soup = BeautifulSoup(r.content, "xml")
                    headlines = [
                        item.title.text
                        for item in soup.find_all("item")[:5]
                        if item.title is not None
                    ]

                    site_name = feed.split("/")[2]
                    file.write(f"\n🌐 {site_name}\n")
                    for h in headlines:
                        file.write(f"- {h}\n")

                    print(f"✅ Logged {len(headlines)} headlines from {site_name}")
                except Exception as e:
                    print(f"⚠️ Failed for {feed}: {e}")

            file.write("\n" + "-" * 60 + "\n")
        print(f"📝 Data logged successfully at {timestamp}")
        time.sleep(86400)  # run once a day


if __name__ == "__main__":
    log_headlines()
