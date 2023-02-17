##import required libraries
import pyspark


def read_movies_table():
    # create Spark session
    spark = pyspark.sql.SparkSession.builder \
        .appName("Read Movies from PostgreSQL") \
        .config('spark.driver.extraClassPath', '/jars/postgresql-42.2.23.jar') \
        # .config("spark.jars.packages", "org.postgresql:postgresql:42.2.23") \
        .getOrCreate()

    # read table from database using Spark JDBC
    movies_df = spark.read.format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/stream") \
        .option("dbtable", "movie") \
        .option("user", "postgres") \
        .option("password", "root") \
        .option("driver", "org.postgresql.Driver") \
        .load()

    # show the dataframe
    movies_df.show()


# if __name__ == '__main__':
    
read_movies_table()
