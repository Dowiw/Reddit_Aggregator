import psycopg2
from textblob import TextBlob

def get_sentiment(text):
    # Return 0.0 if text is empty or None to avoid NULL in DB
    if text and text.strip():
        return TextBlob(text).sentiment.polarity
    return 0.0

# 1. Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="reddit-data",
    user="postgres",
    password="somerandompassword",
    host="localhost"
)
cursor = conn.cursor()

# 2. Fetch posts
cursor.execute("SELECT id, title, selftext, comments FROM reddit_posts")
posts = cursor.fetchall()

for post_id, title, selftext, comments in posts:
    # Compute individual sentiment scores with rounding to 3 decimals
    title_score = round(get_sentiment(title), 3)
    selftext_score = round(get_sentiment(selftext), 3)

    # Comments: average of all sentiments
    comment_scores = []
    if comments:
        for comment in comments:
            score = get_sentiment(comment)
            comment_scores.append(score)
    comment_avg = round(sum(comment_scores) / len(comment_scores), 3) if comment_scores else 0.0

    # Average overall sentiment
    avg_score = (title_score + selftext_score + comment_avg) / 3

    # Determine sentiment label
    if avg_score > 0.2:
        label = "positive"
    elif avg_score < -0.2:
        label = "negative"
    else:
        label = "neutral"

    # Debug print
    print(f"Post ID: {post_id}, Title: {title_score}, Selftext: {selftext_score}, Comments Avg: {comment_avg}, Label: {label}")

    # Update database
    cursor.execute("""
        UPDATE reddit_posts
        SET 
            sentiment_title_score = %s,
            sentiment_selftext_score = %s,
            sentiment_comments_avg_score = %s,
            sentiment_label = %s
        WHERE id = %s
    """, (title_score, selftext_score, comment_avg, label, post_id))

# Commit changes and close
conn.commit()
cursor.close()
conn.close()
print("Sentiment analysis complete.")
