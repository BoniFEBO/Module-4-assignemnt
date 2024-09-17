# Netflix Shows Analysis

This project analyzes Netflix content data using both Python and R. It includes data cleaning, basic analysis, and visualization of key insights from the Netflix shows and movies dataset.

## Dataset

The analysis uses the "Netflix_shows_movies.csv" file, which should be placed in the same directory as the scripts. This dataset contains information about Netflix content, including titles, directors, cast, countries, ratings, and more.

## Python Solution

### Requirements

- Python 3.x
- pandas
- matplotlib
- seaborn

Install the required packages using:
```
pip install pandas matplotlib seaborn
```

### Running the Script

1. Ensure "Netflix_shows_movies.csv" is in the same directory as the script.
2. Run the script

### Output

The Python script generates several PNG files with visualizations:

- netflix_top_genres.png
- netflix_ratings_distribution.png
- netflix_content_type_distribution.png
- netflix_top_producing_countries.png
- netflix_content_growth.png

## R Solution

### Requirements

- R
- tidyverse
- lubridate

Install the required packages in R:

```r
install.packages(c("tidyverse", "lubridate"))
```

Run the script

### Output
The R script generates one PNG file:

netflix_top_genres.png
