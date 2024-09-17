# Netflix Content Analysis in R

# Load required libraries
library(tidyverse)
library(lubridate)

# Function to load and clean data
load_and_clean_data <- function(file_path) {
  # Read CSV file
  netflix_df <- read_csv(file_path)
  
  # Display missing values before cleaning
  cat("Missing values before cleaning:\n")
  print(colSums(is.na(netflix_df)))
  
  # Clean data
  netflix_df <- netflix_df %>%
    mutate(
      director = replace_na(director, "Not Available"),
      cast = replace_na(cast, "Not Available"),
      country = replace_na(country, "Unknown"),
      rating = replace_na(rating, names(which.max(table(rating)))),
      date_added = mdy(str_trim(date_added)),
      date_added = replace_na(date_added, median(date_added, na.rm = TRUE))
    )
  
  # Handle duration
  netflix_df <- netflix_df %>%
    mutate(duration = case_when(
      is.na(duration) & type == "Movie" ~ 
        paste(median(as.numeric(str_extract(duration[type == "Movie"], "\\d+")), na.rm = TRUE), "min"),
      is.na(duration) & type == "TV Show" ~ names(which.max(table(duration[type == "TV Show"]))),
      TRUE ~ duration
    ))
  
  # Display missing values after cleaning
  cat("\nMissing values after cleaning:\n")
  print(colSums(is.na(netflix_df)))
  
  return(netflix_df)
}

# Function to analyze data
analyze_data <- function(df) {
  cat("\nDataset Overview:\n")
  print(str(df))
  
  cat("\nNumerical Data Summary:\n")
  print(summary(df))
}

# Function to visualize data (Top 10 genres)
visualize_top_genres <- function(df) {
  df %>%
    separate_rows(listed_in, sep = ", ") %>%
    count(listed_in, sort = TRUE) %>%
    top_n(10) %>%
    ggplot(aes(x = reorder(listed_in, n), y = n)) +
    geom_bar(stat = "identity", fill = "skyblue") +
    coord_flip() +
    labs(title = "Top 10 Netflix Genres",
         x = "Genre",
         y = "Count") +
    theme_minimal()
  
  ggsave("netflix_top_genres.png", width = 10, height = 6)
}

# Main function
main <- function() {
  netflix_df <- load_and_clean_data("Netflix_shows_movies.csv")
  analyze_data(netflix_df)
  visualize_top_genres(netflix_df)
  cat("Analysis complete. Please check 'netflix_top_genres.png' for visualization.\n")
}

# Run the main function
main()
