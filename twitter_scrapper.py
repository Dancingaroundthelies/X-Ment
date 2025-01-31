from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_tweets(keyword, count=10):
    nitter_url = f"https://nitter.net/search?f=tweets&q={keyword}&lang=en"
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run without opening a browser
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0")
    options.add_argument("--log-level=3")  # Suppress unnecessary logs

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(nitter_url)
    time.sleep(3)
    
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

def get_thread_tweets(tweet_url, count=10):
    tweet_id = tweet_url.split("/")[-1]
    nitter_thread_url = f"https://nitter.net/i/status/{tweet_id}"
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-agent=Mozilla/5.0")
    options.add_argument("--log-level=3")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(nitter_thread_url)
    time.sleep(3)
    
    replies = driver.find_elements(By.CLASS_NAME, "timeline-item")
    replies_data = []

    for reply in replies[:count]:
        try:
            text_element = reply.find_element(By.CLASS_NAME, "tweet-content")
            text = text_element.text.strip()

            link_element = reply.find_element(By.CLASS_NAME, "tweet-link")
            link = link_element.get_attribute("href")
            if not link.startswith("https"):
                link = "https://nitter.net" + link

            replies_data.append({"text": text, "url": link})
        except:
            continue  # Skip replies that couldn't be extracted

    driver.quit()

    return replies_data if replies_data else [{"error": "No replies found"}]