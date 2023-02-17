##import required libraries
import pyspark


 # create Spark session
spark = pyspark.sql.SparkSession.builder \
    .appName("Read Movies from PostgreSQL") \
    .config('spark.driver.extraClassPath', '/jars/postgresql-42.2.23.jar') \
    .getOrCreate()



def extract_movies_to_df():
    # read table from database using Spark JDBC
    movies_df = spark.read.format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/stream") \
        .option("dbtable", "movie") \
        .option("user", "postgres") \
        .option("password", "root") \
        .option("driver", "org.postgresql.Driver") \
        .load()
    return movies_df


def extract_ratings_to_df():
    # read table from database using Spark JDBC
    rating_df = spark.read.format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/stream") \
        .option("dbtable", "rating") \
        .option("user", "postgres") \
        .option("password", "root") \
        .option("driver", "org.postgresql.Driver") \
        .load()
    return rating_df


def transform_avg_ratings(movies_df,  rating_df):
    ## transforming tables
    avg_rating = rating_df.groupBy("movie_id").mean("rating")
    ##join the movies_df and avg_ratings table on id
    df = movies_df.join(avg_rating, movies_df.id == avg_rating.movie_id)
    df = df.drop("movie_id")
    df.show()
    return df


def load_df_to_db(df):
    mode = "overwrite"
    url = "jdbc:postgresql://localhost:5432/stream"
    properties = {"user": "postgres",
                  "password": "root",
                  "driver": "org.postgresql.Driver"
                  }
    df.write.jdbc(url=url,
                  table="avg_ratings",
                  mode=mode,
                  properties=properties)



if __name__ == "__main__":

    movies_df = extract_movies_to_df()
    rating_df = extract_ratings_to_df()
    transform_df = transform_avg_ratings(movies_df, rating_df)
    load_df_to_db(transform_df)
