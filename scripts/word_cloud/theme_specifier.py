import psycopg2
import yake
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Connect to your database
conn = psycopg2.connect(
    dbname="reddit-data",
    user="postgres",
    password="somerandompassword",
    host="localhost"
)
cursor = conn.cursor()

# Fetch posts
cursor.execute("SELECT id, title, selftext FROM reddit_posts WHERE search_context = 'job AND Berlin';")
posts = cursor.fetchall()

# Words to ignore in theme extraction
ignore_words = {"berlin", "germany", "job", "jobs", "work", "berliner", "neutral", "positive", "negative"}

# Simple sentiment word list (expand as needed)
sentiment_words = {
    # Positive
    "happy", "love", "excited", "enjoy", "grateful", "thankful", "proud", "motivated", "confident", "relaxed",
    "comfortable", "smooth", "helpful", "blessing", "best", "wonderful", "amazing", "nice", "good", "lucky", "fun",
    "friendly", "welcoming", "supportive", "appreciate", "recommend", "successful", "easy", "flexible", "affordable",
    "opportunity", "positive", "safe", "secure", "promotion", "salary", "hired", "career", "pay", "wage", "appreciate",
    # Negative
    "frustrated", "tough", "ridiculous", "unlucky", "uncomfortable", "crazy", "psycho", "strict", "disappointed", "sad",
    "anxious", "worried", "stressed", "hard", "aggressive", "annoying", "desperate", "problem", "struggle", "pain",
    "scam", "unfair", "bad", "hate", "difficult", "unsafe", "shock", "tired", "angry", "rejected", "lost", "impossible",
    "vent", "complain", "lonely", "miserable", "depression", "burnout", "broke", "debt", "poor", "expensive",
    "overcharged", "ignored", "ghosted", "jobless", "unemployed", "fired", "waiting", "application", "rejected",
    # Berlin/Reddit/Contextual Jargon
    "rent", "roommate", "landlord", "flat", "apartment", "room", "commute", "study", "degree", "visa", "permit",
    "scam", "ghosted", "burnout", "vent", "promotion", "salary", "unemployed", "jobless", "hired", "fired", "waiting",
    "application", "contract", "cost", "price", "supportive", "welcoming", "flexible", "affordable", "opportunity",
    "positive", "successful", "recommend", "appreciate", "helpful", "friendly", "nice", "good", "lucky", "fun", "best",
    "wonderful", "amazing", "blessing", "smooth", "comfortable", "relaxed", "confident", "motivated", "proud",
    "thankful", "grateful", "enjoy", "excited", "love", "happy"
}

analyzer = SentimentIntensityAnalyzer()
kw_extractor = yake.KeywordExtractor(lan="en", n=1, top=10)

for post_id, title, selftext in posts:
    text = (title or '') + ' ' + (selftext or '')
    if not text.strip():
        theme = ''
    else:
        # Extract keywords, filter out ignore words
        keywords = [kw[0] for kw in kw_extractor.extract_keywords(text)]
        filtered_keywords = [w for w in keywords if w.lower() not in ignore_words]
        # Find sentiment words in filtered keywords
        sentiment_theme = next((w for w in filtered_keywords if w.lower() in sentiment_words), '')
        # Fallback: scan all words in text for sentiment words
        if not sentiment_theme:
            words_in_text = set(word.lower().strip('.,!?') for word in text.split())
            found = words_in_text & sentiment_words
            if found:
                sentiment_theme = found.pop()
        # If still none found, assign positive/negative/neutral
        if not sentiment_theme:
            scores = analyzer.polarity_scores(text)
            if scores['compound'] >= 0.05:
                sentiment_theme = 'positive'
            elif scores['compound'] <= -0.05:
                sentiment_theme = 'negative'
            else:
                sentiment_theme = 'neutral'
        theme = sentiment_theme
    print(f"Post ID: {post_id}, Theme: {theme}")
    cursor.execute(
        "UPDATE reddit_posts SET theme = %s WHERE id = %s;",
        (theme, post_id)
    )

conn.commit()
cursor.close()
conn.close()