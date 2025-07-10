# Reddit Aggregator

Welcome to the Reddit Aggregator project! This repository is a collection of scripts and tools for collecting, cleaning, analyzing, and visualizing Reddit data.

## Requirements
- Python 3.x
- PostgreSQL (for database storage)
- Python libraries in requirements.txt

## Project Structure

Here's a quick overview of what's inside:

### scripts/api/
Note: Do make a Reddit Developer Account and make a praw.ini & replace the psql credentials
- **cleaner.py**: Cleans raw reddit data initially
- **collector.py**: Collects raw data (starting point)
- **import_to_psql.py**: Imports raw data into PostgreSQL
- **raw_to_jsonl.py**: Converts raw Reddit data into JSON Lines format for table-based manipulation

### scripts/mapreduce/
- **mapper.py**: Part of a MapReduce workflow. Breaking down data for distributed processing.
- **reducer.py**: The reducing step of MapReduce, aggregating results from the mapper.

### scripts/sentiment_val/
- **update_sentiment.py**: Analyzes and updates sentiment scores for Reddit posts or comments. Useful for tracking mood or opinion trends.

### scripts/word_cloud/
- **plot_to_cloud.py**: Generates word clouds from Reddit data.
- **theme_specifier.py**: Helps specify or extract themes from Reddit data for more targeted analysis or visualization.

### Other Files
- **queries.sql**: Contains SQL queries for analyzing data in your PostgreSQL database.

## Getting Started
1. Clone the repo and explore the `scripts/` directory.
2. Start with `collector.py` to fetch Reddit data.
3. Clean and process your data with the provided scripts.
4. Import your data into PostgreSQL and run the queries in `queries.sql`.
5. Try out the NLP and visualization tools for deeper insights!

> - Made with Python, PostgreSQL, Hadoop, Tableau
> - By KB, Shukrulloh, Fatih, Ezra
