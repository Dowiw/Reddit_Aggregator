import json


# initial cleaner

# load raw data
with open('student_job_hunt_berlin.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

cleaned_posts = []
seen_ids = set()

for post in posts:
    # remove duplicates
    if post['id'] in seen_ids:
        continue
    seen_ids.add(post['id'])

    # remove deleted or empty posts
    if not post['selftext'] or post['selftext'].lower() in ['[deleted]', '[removed]']:
        continue
    if not post['title']:
        continue
    if post['author'] in ['[deleted]', None]:
        continue

    # normalize text
    post['title'] = post['title'].strip()
    post['selftext'] = post['selftext'].strip()

    # add to cleaned posts
    cleaned_posts.append(post)

# save cleaned data
with open('job_berlin_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_posts, f, indent=2, ensure_ascii=False)

# print out the number of posts removed
print(f"Cleaned posts saved: {len(cleaned_posts)}")