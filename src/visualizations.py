import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def plot_content_type_distribution(df: pd.DataFrame, save_path="output/content_type_distribution.png"):
    type_counts = df['content_category'].value_counts()

    # Matplotlib version
    plt.figure(figsize=(6, 4))
    type_counts.plot(kind='bar', color=['#FF5C5C', '#5C85FF'])
    plt.title("Distribution of Content Type")
    plt.xlabel("Type")
    plt.ylabel("Count")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    print(f"📊 Saved: {save_path}")

    # Plotly version (optional)
    fig = px.pie(type_counts, names=type_counts.index, values=type_counts.values,
                 title="Content Type Distribution (Interactive)")
    fig.write_html("output/content_type_distribution.html")
    print("🌐 Saved: output/content_type_distribution.html")
    
from collections import Counter

def plot_top_genres(df: pd.DataFrame, save_path="output/top_genres.png"):
    genre_list = df['genres'].dropna().sum()  # flatten list of lists
    top_genres = Counter(genre_list).most_common(10)
    genres, counts = zip(*top_genres)

    plt.figure(figsize=(8, 5))
    plt.barh(genres, counts, color="#A569BD")
    plt.xlabel("Count")
    plt.title("Top 10 Genres")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"📊 Saved: {save_path}")


def plot_content_by_year(df: pd.DataFrame, save_path="output/content_by_year.png"):
    year_counts = df['year_added'].value_counts().sort_index()

    plt.figure(figsize=(10, 5))
    year_counts.plot(kind='line', marker='o', color="#3498DB")
    plt.title("Content Added Over Years")
    plt.xlabel("Year Added")
    plt.ylabel("Number of Shows/Movies")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"📊 Saved: {save_path}")
    
