-- Create the table reddit_posts
CREATE TABLE reddit_posts (
    id SERIAL PRIMARY KEY,             -- or just omit if not useful
    submission_id TEXT UNIQUE,         -- Reddit's real post ID
    title TEXT,
    selftext TEXT,
    author TEXT,
    created_utc DOUBLE PRECISION,
    score INTEGER,
    num_comments INTEGER,
    subreddit TEXT,
    search_context TEXT,
    comments TEXT[]                    -- Array of comment bodies (PostgreSQL supports text[])
);

-- delete table if needed
DROP TABLE reddit_posts;

-- show the path of the config for collaboration
SHOW config_file;

-- show hba file for ip permissions
SHOW hba_file;

SELECT * FROM reddit_posts;

-- add columns for sentimental analysis
ALTER TABLE reddit_posts
ADD COLUMN sentiment_title_score DOUBLE PRECISION,
ADD COLUMN sentiment_selftext_score DOUBLE PRECISION,
ADD COLUMN sentiment_comments_avg_score DOUBLE PRECISION,
ADD COLUMN sentiment_label TEXT;

ALTER TABLE reddit_posts
ADD COLUMN theme TEXT;