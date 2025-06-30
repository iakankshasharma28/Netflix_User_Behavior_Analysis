import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Drop rows where 'Title' or 'Type' is missing
    df = df.dropna(subset=['title', 'type'])
    
    # Fill missing 'country' with 'Unknown'
    df['country'] = df['country'].fillna('Unknown')

    # Fill missing 'rating' with 'Not Rated'
    df['rating'] = df['rating'].fillna('Not Rated')

    # Convert 'date_added' to datetime
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

    # Create a new column for 'year_added'
    df['year_added'] = df['date_added'].dt.year

    # Strip spaces from categorical fields
    for col in ['type', 'title', 'director', 'country', 'rating']:
        df[col] = df[col].astype(str).str.strip()

    print("🧽 Data cleaned.")
    return df
