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

-- make readonly user
CREATE USER readonly_user WITH PASSWORD 'readonlypass';
GRANT CONNECT ON DATABASE "reddit-data" TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;

SELECT * FROM reddit_posts;