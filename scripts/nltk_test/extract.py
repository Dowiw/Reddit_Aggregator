import psycopg2
import nltk
from collections import Counter, defaultdict
import json
import re
from textblob import TextBlob

nltk.download('punkt')

# Stricter advice patterns: start-of-sentence, direct advice
advice_patterns = [
    r"^you should\b",
    r"^i recommend\b",
    r"^try to\b",
    r"^consider\b",
    r"^avoid\b",
    r"^my advice\b",
    r"^here'?s a tip\b",
    r"^it's best to\b",
    r"^if i were you\b",
    r"^make sure\b",
    r"^don't forget to\b",
    r"^always\b",
    r"^never\b",
    r"^the best way\b",
    r"^one thing you should\b",
    r"^remember to\b",
    r"^ensure that\b",
    r"^be sure to\b"
]

def is_advice_sentence(sentence):
    # Exclude questions
    if sentence.strip().endswith("?"):
        return False
    # Match advice patterns at the start of the sentence
    for pat in advice_patterns:
        if re.match(pat, sentence.strip(), re.IGNORECASE):
            # Optional: Only keep if subjective enough
            if TextBlob(sentence).sentiment.subjectivity > 0.4:
                return True
    return False

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="reddit-data",
    user="postgres",
    password="somerandompassword",
    host="localhost"
)

cursor = conn.cursor()
cursor.execute("""
    SELECT title, selftext, comments, to_char(to_timestamp(created_utc), 'YYYY') AS year
    FROM reddit_posts
    WHERE search_context = 'job AND Berlin';
""")
rows = cursor.fetchall()

advice_per_year = defaultdict(list)

for title, selftext, comments, year in rows:
    text = (title or '') + ' ' + (selftext or '')
    # If comments is a stringified dict, parse it
    if comments and isinstance(comments, str) and comments.startswith('{'):
        try:
            comments_list = list(json.loads(comments).values())
            text += ' ' + ' '.join(comments_list)
        except Exception:
            pass
    elif comments and isinstance(comments, list):
        text += ' ' + ' '.join(comments)
    # Split into sentences
    sentences = nltk.sent_tokenize(text)
    for sent in sentences:
        if is_advice_sentence(sent):
            advice_per_year[year].append(sent.strip())

# Count most common advice sentences per year
for year in sorted(advice_per_year):
    print(f"\nYear: {year}")
    counter = Counter(advice_per_year[year])
    for advice, count in counter.most_common(10):
        print(f"{count}x: {advice}")