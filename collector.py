import praw
import json

# Search for job posts in Berlin on Reddit using PRAW (Python Reddit API Wrapper)

# open the reddit api using praw
reddit = praw.Reddit()
# note: praw will look for a file called praw.ini that contains your credentials

# define search parameters

# query about entry, job hunting as a student in Germany
searches = [
    {
        "query": 'job AND Berlin',
        "subreddits": ["berlin", "germany", "de", "expats", "IWantOut", "europe", "AskEurope", "German", "askberliners", "Germany_Jobs"]
    }
]

i = 0  # post id counter
max_posts = 300  # per search

posts = []
for search in searches:
    for sub in search["subreddits"]:
        print(f"Searching in subreddit: {sub}") # print current subreddit searched
        for submission in reddit.subreddit(sub).search(search["query"], sort='new', limit=max_posts):
            submission.comments.replace_more(limit=0)  # flatten comment tree
            comments = [comment.body for comment in submission.comments.list()]
            posts.append({
                'id': i,
                'title': submission.title,
                'selftext': submission.selftext,
                'author': str(submission.author),
                'created_utc': submission.created_utc,
                'score': submission.score,
                'num_comments': submission.num_comments,
                'subreddit': str(submission.subreddit),
                'submission_id': submission.id,
                'search_context': search["query"],
                'comments': comments
            })
            i += 1  # increment post id counter
            print(f"Post ID {i}: {submission.title} (Author: {submission.author})")  # print post id and title

# save data to JSON
with open('job_berlin.json', 'w', encoding='utf-8') as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)