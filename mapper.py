import sys, json, re

# Simple stopword list; replace/expand as needed
STOPWORDS = set([
    "i", "me", "my", "we", "our", "you", "your", "the", "a", "an", "and", "or", "in", "on", "at", "to", "for"
])

def clean_text(text):
    if not text:
        return ""
    text = text.lower().strip()
    # Remove URLs
    text = re.sub(r"http\S+", "", text)
    # Keep only ASCII characters
    text = text.encode("ascii", "ignore").decode("ascii")
    # Remove stopwords
    text = " ".join([w for w in text.split() if w not in STOPWORDS])
    return text

for line in sys.stdin:
    try:
        post = json.loads(line)
        # Required fields check
        if not post.get("id") or not post.get("selftext") or post["selftext"].lower() in ["[removed]", "[deleted]"]:
            continue
        # Normalize text fields
        post['title'] = clean_text(post.get('title', ''))
        post['selftext'] = clean_text(post.get('selftext', ''))
        post['comments'] = [clean_text(comment) for comment in post.get('comments', [])]
        # Remove empty posts after cleaning
        if not post['selftext'] and not post['title']:
            continue
        print(f"{post['id']}\t{json.dumps(post, ensure_ascii=False)}")
    except Exception:
        continue