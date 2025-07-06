from wordcloud import WordCloud
import matplotlib.pyplot as plt
import psycopg2
import os
from collections import Counter

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
print(f"Font exists: {os.path.isfile(font_path)}")

# Connect to your database
conn = psycopg2.connect(
    dbname="reddit-data",
    user="postgres",
    password="somerandompassword",
    host="localhost"
)
cursor = conn.cursor()

# Fetch all themes
cursor.execute("SELECT theme FROM reddit_posts WHERE theme IS NOT NULL AND theme != '';")
themes = [row[0] for row in cursor.fetchall()]

# Count frequency of each theme
theme_counts = Counter(themes)

# Debugging output
print(f"Number of unique themes: {len(theme_counts)}")
print(f"Most common themes: {theme_counts.most_common(10)}")

# Generate the word cloud from frequencies
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    font_path=font_path,
    collocations=False,
    margin=1,
    min_font_size=6,
    max_words=200
).generate_from_frequencies(theme_counts)

# Display the word cloud
plt.figure(figsize=(14, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Most Common Themes in Berlin Job Posts')
plt.tight_layout(pad=0)
plt.show()

cursor.close()
conn.close()