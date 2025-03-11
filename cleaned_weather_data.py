import sys
import json
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import count, avg

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

input_path = "s3://crypto-project-demo/weather/weather_raw/states_weather_history_meteostat.json"
output_path = "s3://crypto-project-demo/weather/cataloged_data/"

json_str = sc.wholeTextFiles(input_path).collect()[0][1]

data = json.loads(json_str)

records = []
for state, dates in data.items():
    for date, metrics in dates.items():
        record = {"state": state, "date": date}
        record.update(metrics)
        records.append(record)

df = spark.createDataFrame(records)

analysis_df = df.groupBy("state").agg(
    count("date").alias("record_count"),
    avg("tavg").alias("avg_tavg"),
    avg("tmin").alias("avg_tmin"),
    avg("tmax").alias("avg_tmax")
)
analysis_df.show()

dyf = DynamicFrame.fromDF(df, glueContext, "dyf")

glueContext.write_dynamic_frame.from_options(
    frame=dyf,
    connection_type="s3",
    connection_options={"path": output_path, "partitionKeys": ["state"]},
    format="parquet"
)

job.commit()
