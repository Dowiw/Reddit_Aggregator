import sys

last_id = None
for line in sys.stdin:
    try:
        post_id, post_json = line.strip().split('\t', 1)
        # Only emit the first post with a given ID (removes duplicates)
        if post_id != last_id:
            print(post_json)
            last_id = post_id
    except Exception:
        continue