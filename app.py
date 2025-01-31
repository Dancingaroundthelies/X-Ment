import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from twitter_scrapper import get_tweets, get_thread_tweets
from sentiment import analyze_sentiment

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "API is running! Available endpoints: /tweets, /thread, /analyze"

@app.route("/tweets", methods=["GET"])
def fetch_tweets():
    keyword = request.args.get("keyword", "")
    count = int(request.args.get("count", 5))
    
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400
    
    tweets = get_tweets(keyword, count)
    
    if not tweets or "error" in tweets[0]:
        return jsonify({"error": "No tweets found"}), 404
    
    return jsonify(tweets)

@app.route("/thread", methods=["GET"])
def fetch_thread():
    tweet_url = request.args.get("url", "")
    count = int(request.args.get("count", 5))
    
    if not tweet_url:
        return jsonify({"error": "Tweet URL is required"}), 400
    
    tweets = get_thread_tweets(tweet_url, count)
    
    if not tweets or "error" in tweets[0]:
        return jsonify({"error": "No replies found"}), 404
    
    return jsonify(tweets)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    texts = data.get("texts", [])
    
    if not texts or not isinstance(texts, list):
        return jsonify({"error": "List of texts is required"}), 400
    
    sentiment = [{"text": text, "sentiment": analyze_sentiment(text)} for text in texts]
    
    return jsonify(sentiment)


if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)