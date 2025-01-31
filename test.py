from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_tweets(keyword, count=10):
    nitter_url = f"https://nitter.net/search?f=tweets&q={keyword}&lang=en"

    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0")
    options.add_argument("--log-level=3")  # Suppress unnecessary logs

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Open Nitter search page
    driver.get(nitter_url)
    time.sleep(3)  # Wait for page to load

    # Find tweet elements
    tweets_data = []
    tweets = driver.find_elements(By.CLASS_NAME, "timeline-item")

    for tweet in tweets[:count]:
        try:
            text_element = tweet.find_element(By.CLASS_NAME, "tweet-content")
            text = text_element.text.strip()

            link_element = tweet.find_element(By.CLASS_NAME, "tweet-link")
            link = link_element.get_attribute("href")
            if not link.startswith("https"):
                link = "https://nitter.net" + link  # Fix duplicate URL issue

            tweets_data.append({"text": text, "url": link})
        except:
            continue  # Skip tweets that couldn't be extracted

    driver.quit()

    return tweets_data if tweets_data else [{"error": "No tweets found"}]

if __name__ == "__main__":
    print(get_tweets("aiesec", count=5))
