import praw
import json

# open the reddit api using praw
reddit = praw.Reddit()
# note: praw will look for a file called praw.ini that contains your credentials

# define search parameters

# query about entry, job hunting as a student in Germany
searches = [
    {
        "query": '"job hunting" OR "finding a job" OR "student job" OR "part time job" AND student AND Berlin',
        "subreddits": ["berlin", "germany", "de", "expats", "IWantOut", "europe", "AskEurope", "German", "askberliners", "Germany_Jobs"]
    }
]

max_posts = 300  # per search

posts = []
for search in searches:
    for sub in search["subreddits"]:
        print(f"Searching in subreddit: {sub}") # print current subreddit searched
        for submission in reddit.subreddit(sub).search(search["query"], sort='new', limit=max_posts):
            posts.append({
                'title': submission.title,
                'selftext': submission.selftext,
                'author': str(submission.author),
                'created_utc': submission.created_utc,
                'score': submission.score,
                'url': submission.url,
                'num_comments': submission.num_comments,
                'subreddit': str(submission.subreddit),
                'id': submission.id,
                'search_context': search["query"]
            })

# save data to JSON
with open('reddit_germany_berlin_joblife.json', 'w', encoding='utf-8') as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)