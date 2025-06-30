import pandas as pd

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    # Split duration into numeric minutes (if applicable)
    if 'duration' in df.columns:
        df['duration_mins'] = df['duration'].str.extract('(\d+)').astype(float)
    
    # Extract year from release_date (if available)
    if 'release_year' not in df.columns and 'release_date' in df.columns:
        df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year

    # Create 'content_category' (Movie or TV Show)
    df['content_category'] = df['type'].apply(lambda x: 'Movie' if x == 'Movie' else 'TV Show')

    # Create genre/keyword list column
    if 'listed_in' in df.columns:
        df['genres'] = df['listed_in'].astype(str).str.split(', ')

    print("✨ Feature engineering completed.")
    return df
