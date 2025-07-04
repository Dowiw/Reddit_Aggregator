import json
import psycopg2

DB_PARAMS = {
    "dbname": "reddit-data",
    "user": "postgres",         # change this!
    "password": "somerandompassword",    # change this!
    "host": "localhost",            # change if needed
    "port": 5432
}

INPUT_FILE = "part-00000"  # Path to your MapReduce output file

def main():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            post = json.loads(line)
            # Ensure comments is a list/array for psycopg2
            comments = post.get("comments", [])
            if comments is None:
                comments = []
            cur.execute("""
                INSERT INTO reddit_posts (
                    id, submission_id, title, selftext, author, created_utc, score,
                    num_comments, subreddit, search_context, comments
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (submission_id) DO NOTHING
            """, (
                post.get("id"),
                post.get("submission_id"),
                post.get("title"),
                post.get("selftext"),
                post.get("author"),
                post.get("created_utc"),
                post.get("score"),
                post.get("num_comments"),
                post.get("subreddit"),
                post.get("search_context"),
                comments
            ))
    conn.commit()
    cur.close()
    conn.close()
    print("Import complete.")

if __name__ == "__main__":
    main()