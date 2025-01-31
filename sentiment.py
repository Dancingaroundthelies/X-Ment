from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity
    
    if sentiment_score > 0:
        sentiment = "Positive 😃"
    elif sentiment_score < 0:
        sentiment = "Negative 😠"
    else:
        sentiment = "Neutral 😶"
        
    return {"text": text, "sentiment": sentiment, "score": sentiment_score}