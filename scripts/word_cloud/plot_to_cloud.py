from wordcloud import WordCloud
import matplotlib.pyplot as plt
import psycopg2
import os

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

# Combine all themes into a single string
text = ' '.join(themes)

# Debugging output
print(f"Number of themes: {len(themes)}")
print(f"Sample text: {text[:100]}")

# Generate the word cloud
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    font_path=font_path
).generate(text)

# Display the word cloud
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Most Common Themes in Berlin Job Posts')
plt.show()

cursor.close()
conn.close()