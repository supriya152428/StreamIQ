import pandas as pd
import psycopg2
from io import StringIO


# ==================================================
# 1. LOAD CLEANED NETFLIX DATA
# ==================================================

csv_path = "../data/output/netflix_cleaned.csv"

df = pd.read_csv(csv_path)

print("CSV loaded successfully!")
print("Rows:", len(df))


# ==================================================
# 2. FIX INTEGER COLUMNS
# ==================================================

integer_columns = [
    "release_year",
    "year_added",
    "month_added",
    "quarter_added",
    "duration_value"
]

for column in integer_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    ).astype("Int64")

print("\nInteger columns cleaned successfully!")


# ==================================================
# 3. HANDLE MISSING VALUES
# ==================================================

df = df.astype(object).where(
    pd.notna(df),
    None
)

print("Missing values handled successfully!")


# ==================================================
# 4. LOAD GENRE DATA
# ==================================================

genre_path = "../data/output/netflix_genres.csv"

genre_df = pd.read_csv(genre_path)

print("\nGenre CSV loaded successfully!")
print("Genre rows:", len(genre_df))

genre_df = genre_df.astype(object).where(
    pd.notna(genre_df),
    None
)


# ==================================================
# 5. LOAD COUNTRY DATA
# ==================================================

country_path = "../data/output/netflix_countries.csv"

country_df = pd.read_csv(country_path)

print("\nCountry CSV loaded successfully!")
print("Country rows:", len(country_df))

country_df = country_df.astype(object).where(
    pd.notna(country_df),
    None
)


# ==================================================
# 6. CONNECT TO POSTGRESQL
# ==================================================

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="streamiq",
    user="postgres",
    password="suppu1528"
)

cursor = conn.cursor()

print("\nConnected to PostgreSQL successfully!")


# ==================================================
# 7. CLEAR EXISTING MAIN TABLE DATA
# ==================================================

cursor.execute(
    "TRUNCATE TABLE netflix_titles;"
)

print("Existing netflix_titles data cleared.")


# ==================================================
# 8. LOAD NETFLIX TITLES INTO MEMORY BUFFER
# ==================================================

csv_buffer = StringIO()

df.to_csv(
    csv_buffer,
    index=False
)

csv_buffer.seek(0)


# ==================================================
# 9. INSERT NETFLIX TITLES
# ==================================================

cursor.copy_expert(
    """
    COPY netflix_titles (
        show_id,
        type,
        title,
        director,
        cast_members,
        country,
        date_added,
        release_year,
        rating,
        duration,
        listed_in,
        description,
        year_added,
        month_added,
        month_name,
        quarter_added,
        duration_value,
        duration_unit
    )
    FROM STDIN
    WITH (
        FORMAT CSV,
        HEADER TRUE,
        DELIMITER ',',
        NULL ''
    );
    """,
    csv_buffer
)

print(f"Loaded {len(df)} rows into netflix_titles.")


# ==================================================
# 10. CLEAR EXISTING GENRE DATA
# ==================================================

cursor.execute(
    "TRUNCATE TABLE netflix_genres;"
)

print("Existing netflix_genres data cleared.")


# ==================================================
# 11. LOAD GENRE DATA INTO MEMORY BUFFER
# ==================================================

genre_buffer = StringIO()

genre_df.to_csv(
    genre_buffer,
    index=False
)

genre_buffer.seek(0)


# ==================================================
# 12. INSERT GENRE DATA
# ==================================================

cursor.copy_expert(
    """
    COPY netflix_genres (
        show_id,
        genre
    )
    FROM STDIN
    WITH (
        FORMAT CSV,
        HEADER TRUE,
        DELIMITER ',',
        NULL ''
    );
    """,
    genre_buffer
)

print(f"Loaded {len(genre_df)} rows into netflix_genres.")


# ==================================================
# 13. CLEAR EXISTING COUNTRY DATA
# ==================================================

cursor.execute(
    "TRUNCATE TABLE netflix_countries;"
)

print("Existing netflix_countries data cleared.")


# ==================================================
# 14. LOAD COUNTRY DATA INTO MEMORY BUFFER
# ==================================================

country_buffer = StringIO()

country_df.to_csv(
    country_buffer,
    index=False
)

country_buffer.seek(0)


# ==================================================
# 15. INSERT COUNTRY DATA
# ==================================================

cursor.copy_expert(
    """
    COPY netflix_countries (
        show_id,
        country
    )
    FROM STDIN
    WITH (
        FORMAT CSV,
        HEADER TRUE,
        DELIMITER ',',
        NULL ''
    );
    """,
    country_buffer
)

print(f"Loaded {len(country_df)} rows into netflix_countries.")


# ==================================================
# 16. COMMIT ALL CHANGES
# ==================================================

conn.commit()

print("\n======================================")
print("PostgreSQL loading completed!")
print("======================================")
print(f"Netflix titles   : {len(df)}")
print(f"Genre records    : {len(genre_df)}")
print(f"Country records  : {len(country_df)}")
print("======================================")


# ==================================================
# 17. CLOSE CONNECTION
# ==================================================

cursor.close()
conn.close()

print("\nPostgreSQL connection closed.")
print("ETL → PostgreSQL completed successfully!")