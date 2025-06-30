import pandas as pd

def load_data(filepath: str) -> pd.DataFrame:
    """Loads Netflix dataset from a CSV file."""
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Data loaded successfully with {df.shape[0]} rows and {df.shape[1]} columns.")
        return df
    except FileNotFoundError:
        print("❌ File not found.")
        return pd.DataFrame()

from src.data_loader import load_data

def explore_data(df):
    print("\n🔍 First 5 rows:")
    print(df.head())
    
    print("\n📊 Dataset Info:")
    print(df.info())
    
    print("\n🧼 Missing Values:")
    print(df.isnull().sum())

def main():
    filepath = 'data/netflix_data.csv'
    df = load_data(filepath)
    explore_data(df)

if __name__ == "__main__":
    main()
    
