from src.data_loader import load_data
from src.cleaning import clean_data
from src.feature_engineering import add_features
from src.visualizations import (
    plot_content_type_distribution,
    plot_top_genres,
    plot_content_by_year
)

def explore_data(df):
    print("\n🔍 First 5 rows:")
    print(df.head())

    print("\n📊 Dataset Info:")
    print(df.info())

    print("\n🧼 Missing Values:")
    print(df.isnull().sum())

def main():
    filepath = 'data/netflix_titles.csv'
    print("📥 Loading Data...")
    df = load_data(filepath)

    if df.empty:
        print("⚠️ The dataset is empty. Please check the file path or content.")
        return

    print("\n🔎 Exploring Raw Data:")
    explore_data(df)

    print("\n🧽 Cleaning Data...")
    df = clean_data(df)

    print("\n🧠 Adding Features...")
    df = add_features(df)

    print("\n📈 Generating Visualizations...")
    plot_content_type_distribution(df)
    plot_top_genres(df)
    plot_content_by_year(df)

if __name__ == "__main__":
    main()
