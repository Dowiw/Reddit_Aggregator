import psycopg2
import yake

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

kw_extractor = yake.KeywordExtractor(lan="en", n=1, top=1)

for post_id, title, selftext in posts:
    text = (title or '') + ' ' + (selftext or '')
    if not text.strip():
        theme = ''
    else:
        keywords = kw_extractor.extract_keywords(text)
        theme = keywords[0][0] if keywords else ''
    print(f"Post ID: {post_id}, Theme: {theme}")
    # Update the theme column for this post
    cursor.execute(
        "UPDATE reddit_posts SET theme = %s WHERE id = %s;",
        (theme, post_id)
    )

conn.commit()
cursor.close()
conn.close()