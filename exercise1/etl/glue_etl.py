import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.context import SparkContext
from pyspark.sql.functions import unix_timestamp

## @params: [JOB_NAME,S3_CSV_OUTPUT_PATH]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_CSV_OUTPUT_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load JSON files into dynamic frame.
datasource0 = glueContext.create_dynamic_frame_from_options("s3", {'paths': ["s3://segment-personalize-workshop/segment-logs"], 'recurse':True}, format="json")
print("Input file total record count: ", datasource0.count())

# Filters the JSON documents that we want included in the output CSV.
# These are the event types we're interested for our dataset.
supported_events = ['Product Added', 'Order Completed', 'Product Clicked']
def filter_function(dynamicRecord):
	if ('userId' in dynamicRecord and
			'properties' in dynamicRecord and
			'sku' in dynamicRecord["properties"] and
			'event' in dynamicRecord and
			dynamicRecord['event'] in supported_events):
		return True
	else:
		return False

# Apply filter function to dynamic frame
interactions = Filter.apply(frame = datasource0, f = filter_function, transformation_ctx = "interactions")
print("Filtered record count: ", interactions.count())

# Map only the fields we want in the output CSV, changing names to match target schema.
applymapping1 = ApplyMapping.apply(frame = interactions, mappings = [ \
	("userId", "string", "USER_ID", "string"), \
	("properties.sku", "string", "ITEM_ID", "string"), \
	("event", "string", "EVENT_TYPE", "string"), \
	("timestamp", "string", "TIMESTAMP_ISO", "string")], \
	transformation_ctx = "applymapping1")

# Repartition to a single file since that is what is required by Personalize
onepartitionDF = applymapping1.toDF().repartition(1)
# Coalesce timestamp into unix timestamp
onepartitionDF = onepartitionDF.withColumn("TIMESTAMP", \
	unix_timestamp(onepartitionDF['TIMESTAMP_ISO'], "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'"))
# Convert back to dynamic frame
onepartition = DynamicFrame.fromDF(onepartitionDF, glueContext, "onepartition_df")
# Drop the ISO formatted timestamp
onepartition = onepartition.drop_fields(['TIMESTAMP_ISO'])

# Write output back to S3 as a CSV
glueContext.write_dynamic_frame.from_options(frame = onepartition, connection_type = "s3", \
	connection_options = {"path": args['S3_CSV_OUTPUT_PATH']}, \
	format = "csv", transformation_ctx = "datasink2")

job.commit()