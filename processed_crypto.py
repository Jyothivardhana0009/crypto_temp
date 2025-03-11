from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql.functions import col, explode, lit, to_date, arrays_zip
from pyspark.sql.types import LongType
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session


crypto_input_path = "s3://crypto-project-demo/weather/crypto_raw/selected_cryptos_historical_data.json"
crypto_raw_df = spark.read.option("multiline", "true").json(crypto_input_path)


coin_names = crypto_raw_df.columns  

crypto_dfs = []
for coin in coin_names:
   
    coin_zipped_df = crypto_raw_df.selectExpr(f"arrays_zip({coin}.prices) as zipped")
    
    coin_exploded_df = coin_zipped_df.select(explode("zipped").alias("entry"))
    
    coin_flat_df = coin_exploded_df.select(
        col("entry.prices").getItem(0).cast(LongType()).alias("timestamp_ms"),
        col("entry.prices").getItem(1).alias("price")
    )

    coin_flat_df = coin_flat_df.withColumn("coin", lit(coin))

    coin_flat_df = coin_flat_df.withColumn("timestamp", (col("timestamp_ms") / 1000).cast("timestamp")) \
                               .withColumn("date", to_date("timestamp"))

    coin_flat_df = coin_flat_df.select("coin", "price", "date")
    crypto_dfs.append(coin_flat_df)


crypto_union_df = crypto_dfs[0]
for cdf in crypto_dfs[1:]:
    crypto_union_df = crypto_union_df.unionByName(cdf)


crypto_output_path = "s3://crypto-project-demo/weather/processed_crypto/"
crypto_union_df.write.mode("overwrite").partitionBy("date").parquet(crypto_output_path)
