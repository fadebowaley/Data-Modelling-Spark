##import required libraries
import pyspark

##create spark session
spark = pyspark.sql.SparkSession \
   .builder \
   .appName("Python Spark SQL basic example") \
   .config('spark.driver.extraClassPath', "/Users/harshittyagi/Downloads/postgresql-42.2.18.jar") \
   .getOrCreate()


##read table from db using spark jdbc
movies_df = spark.read \
   .format("jdbc") \
   .option("url", "jdbc:postgresql://localhost:5432/stream") \
   .option("dbtable", "movies") \
   .option("user", "postgres") \
   .option("password", "root") \
   .option("driver", "org.postgresql.Driver") \
   .load()

##print the movies_df
print(movies_df.show())


