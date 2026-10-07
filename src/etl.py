import pandas as pd
import numpy as np

df = pd.read_excel(
    "../data/input/StreamIQ_Netflix_Analytics.xlsx",
    sheet_name="Cleaned_Data"
)

print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

original_dates = df["date_added"].copy()

df["date_added"] = pd.to_datetime(
    df["date_added"],
    format="mixed",
    errors="coerce"
)

invalid_dates = original_dates[
    df["date_added"].isna() & original_dates.notna()
]

print("\nInvalid Date Values:")
print(invalid_dates.to_string())

print("\nNumber of Invalid Date Values:")
print(len(invalid_dates))

# Feature engineering: date-based columns

df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month
df["month_name"] = df["date_added"].dt.month_name()
df["quarter_added"] = df["date_added"].dt.quarter

print("\nNew Date Features:")
print(df[[
    "date_added",
    "year_added",
    "month_added",
    "month_name",
    "quarter_added"
]].head(10))

genre_df = df[["show_id", "listed_in"]].copy()

genre_df["genre"] = genre_df["listed_in"].str.split(", ")

genre_df = genre_df.explode("genre")

genre_df = genre_df[["show_id", "genre"]]

print("\nNormalized Genre Data:")
print(genre_df.head(10))

print("\nNumber of Genre Records:")
print(len(genre_df))

country_df = df[["show_id", "country"]].copy()

country_df["country"] = country_df["country"].str.split(", ")

country_df = country_df.explode("country")

country_df = country_df[["show_id", "country"]]

print("\nNormalized Country Data:")
print(country_df.head(10))

print("\nNumber of Country Records:")
print(len(country_df))

df["duration_value"] = (
    df["duration"]
    .str.extract(r"(\d+)")
    .astype("Int64")
)

df["duration_unit"] = (
    df["duration"]
    .str.extract(r"([A-Za-z]+)")
)

print("\nDuration Features:")
print(df[[
    "title",
    "duration",
    "duration_value",
    "duration_unit"
]].head(10))

print("\nFinal Shape:", df.shape)
print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())


# Export main cleaned dataset
df.to_csv(
    "../data/output/netflix_cleaned.csv",
    index=False
)

# Export normalized genres
genre_df.to_csv(
    "../data/output/netflix_genres.csv",
    index=False
)

# Export normalized countries
country_df.to_csv(
    "../data/output/netflix_countries.csv",
    index=False
)

print("\nPython ETL completed successfully!")
print("Files exported to data/output/")