import requests
import time

websites = ["https://deepmonapara.dev"]


def check_website(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {url} is UP! ({response.elapsed.total_seconds()}s)")
        else:
            print(f"⚠️ {url} returned status {response.status_code}")
    except requests.exceptions.RequestException:
        print(f"❌ {url} is DOWN!")


if __name__ == "__main__":
    while True:
        print("🔍 Checking website health...\n")
        for site in websites:
            check_website(site)
        print("-" * 40)
        time.sleep(30)  # checks every 30 seconds
