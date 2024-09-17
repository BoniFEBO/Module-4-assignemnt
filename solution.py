import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_clean_data(file_path):
    # Load data
    netflix_df = pd.read_csv(file_path)
    
    print("Missing values before cleaning:")
    print(netflix_df.isnull().sum())

    # Clean data
    netflix_df['director'].fillna('Not Available', inplace=True)
    netflix_df['cast'].fillna('Not Available', inplace=True)
    netflix_df['country'].fillna('Unknown', inplace=True)
    netflix_df['rating'].fillna(netflix_df['rating'].mode()[0], inplace=True)

    # Handle duration
    netflix_df['duration'] = netflix_df.apply(lambda row: clean_duration_field(row, netflix_df), axis=1)

    # Clean date_added
    netflix_df['date_added'] = pd.to_datetime(netflix_df['date_added'].str.strip(), format='%B %d, %Y', errors='coerce')
    netflix_df['date_added'].fillna(netflix_df['date_added'].mode()[0], inplace=True)

    # Convert data types
    netflix_df = convert_data_types(netflix_df)

    print("\nMissing values after cleaning:")
    print(netflix_df.isnull().sum())

    return netflix_df

def clean_duration_field(row, df):
    if pd.isna(row['duration']):
        if row['type'] == 'Movie':
            return f"{df[df['type'] == 'Movie']['duration'].str.extract('(\d+)').astype(float).median()[0].astype(int)} min"
        else:
            return df[df['type'] == 'TV Show']['duration'].mode()[0]
    return row['duration']

def convert_data_types(df):
    type_mapping = {
        'show_id': 'string',
        'type': 'category',
        'title': 'string',
        'director': 'string',
        'cast': 'string',
        'country': 'string',
        'release_year': 'int',
        'rating': 'category',
        'duration': 'string',
        'listed_in': 'string',
        'description': 'string'
    }
    return df.astype(type_mapping)

def analyze_data(df):
    print("\nDataset Overview:")
    print(df.info())

    print("\nNumerical Data Summary:")
    print(df.describe())

def visualize_data(df):
    # Top genres
    plt.figure(figsize=(12, 6))
    genre_data = df['listed_in'].str.split(', ', expand=True).stack().value_counts().head(10)
    sns.barplot(x=genre_data.index, y=genre_data.values)
    plt.title('Top 10 Netflix Genres')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('netflix_top_genres.png')
    plt.close()

    # Rating distribution
    plt.figure(figsize=(10, 6))
    sns.countplot(x='rating', data=df, order=df['rating'].value_counts().index)
    plt.title('Netflix Content Ratings Distribution')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('netflix_ratings_distribution.png')
    plt.close()

    # Content type distribution
    plt.figure(figsize=(8, 6))
    df['type'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Netflix Content Type Distribution')
    plt.ylabel('')
    plt.savefig('netflix_content_type_distribution.png')
    plt.close()

    # Top producing countries
    plt.figure(figsize=(12, 6))
    country_data = df['country'].str.split(', ', expand=True).stack().value_counts().head(10)
    sns.barplot(x=country_data.index, y=country_data.values)
    plt.title('Top 10 Countries Producing Netflix Content')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('netflix_top_producing_countries.png')
    plt.close()

    # Content growth over time
    df['year_added'] = df['date_added'].dt.year
    yearly_growth = df['year_added'].value_counts().sort_index()
    plt.figure(figsize=(12, 6))
    yearly_growth.plot(kind='line', marker='o')
    plt.title('Netflix Content Growth Over Time')
    plt.xlabel('Year')
    plt.ylabel('Titles Added')
    plt.tight_layout()
    plt.savefig('netflix_content_growth.png')
    plt.close()

def main():
    netflix_df = load_and_clean_data('Netflix_shows_movies.csv')
    analyze_data(netflix_df)
    visualize_data(netflix_df)
    print("Analysis complete. Please check the generated PNG files for visualizations.")

if __name__ == "__main__":
    main()
