import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from pyspark.sql.functions import unix_timestamp

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_JSON_INPUT_PATH', 'S3_CSV_OUTPUT_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

datasource0 = glueContext.create_dynamic_frame.from_options('s3', {'paths': [args['S3_JSON_INPUT_PATH']]}, 'json')
print("Input file: ", args['S3_JSON_INPUT_PATH'])
print("Input file total record count: ", datasource0.count())

def filter_function(dynamicRecord):
	if dynamicRecord["properties"]["sku"] and dynamicRecord["userId"]:
		return True
	else:
		return False

interactions = Filter.apply(frame = datasource0, f = filter_function, transformation_ctx = "interactions")
print("Filtered record count: ", interactions.count())

applymapping1 = ApplyMapping.apply(frame = interactions, mappings = [("anonymousId", "string", "ANONYMOUS_ID", "string"),("userId", "string", "USER_ID", "string"),("properties.sku", "string", "ITEM_ID", "string"),("event", "string", "EVENT_TYPE", "string"),("timestamp", "string", "TIMESTAMP_ISO", "string")], transformation_ctx = "applymapping1")

# Repartition to a single file
onepartitionDF = applymapping1.toDF().repartition(1)
# Coalesce timestamp into unix timestamp
onepartitionDF = onepartitionDF.withColumn("TIMESTAMP", unix_timestamp(onepartitionDF['TIMESTAMP_ISO'], "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'"))
# Convert back to dyanmic frame
onepartition = DynamicFrame.fromDF(onepartitionDF, glueContext, "onepartition_df")

glueContext.write_dynamic_frame.from_options(frame = onepartition, connection_type = "s3", connection_options = {"path": args['S3_CSV_OUTPUT_PATH']}, format = "csv", transformation_ctx = "datasink2")

job.commit()