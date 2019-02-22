# Exercise 1 - Data Transformation, Exploration, and Upload into Personalize Dataset Group

The ability of machine learning models to make effective recommendations is heavily influenced by the quantity and quality of data input during the training process. For most personalization ML solutions, training data typically comes from clickstream data collected from websites, mobile applications, and other online & offline channels where end-users are interacting with items for which we wish to make recommendations. Examples of clickstream events include viewing items, adding items to a list or cart, and of course purchasing items. Although an Amazon Personalize Campaign can be started with just new clickstream data going forward, the initial quality of the recommendations will not be as high as a model that has been trained on recent historical data.

One of Segment's core capabilities is the ability collect
In this exercise we will walk through the process required to take historical clickstream data collected by Segment to train a model in Amazon Personalize. The advantage of bootstrapping Personalize with historical clickstream data is that you will start with a model that has the benefit of This will Segment provides the ability to send event data from one or more data sources configured in your Segment account to several AWS services including S3, Kinesis, and Redshift. Since the raw format, fields, and event types in the Segment event data cannot be directly uploaded to Amazon Personalize for model training, this exercise will guide you through the process of transforming the data into the format expected by Personalize. We will start with raw event data that has already aggregated into a single JSON file in a S3 bucket. We will use AWS Glue to create an ETL (extract, transform, load) job that will take the JSON file, apply filtering and field mapping to each JSON event, and write the output back to S3 as a CSV file.

## Setup Environment

1. Install and configure AWS CLI.
2. Download access key and secret to configure CLI.

## Data Preparation

1. Copy raw events file to your S3 bucket.

aws s3 cp s3://segment-personalize-data/raw-events/events.json s3://personalize-data-224124347618/raw-events/events.json

2. Create Glue Job to transform the raw events to CSV.

- Log in to AWS console.
- Browse to AWS Glue service.
- Ensure region is set to us-east-1 (N Virginia)
- Click "Jobs" in left navigation.
- Click "Add job" button.
     - Enter a job name such as "SegmentEventsJsonToCsv"
     - For IAM role, select "SegmentPersonalizeWorkshop-GlueServiceRole-..."
     - Leave Type as "Spark".
     - For "This job runs", click the radio button "A new script to be authored by you".
     - Leave everything else the same and click Next.
     - On the "Connections" step just click "Save job and edit script" since we are not accessing data in a database.
     - Open the file "GlueETL.py" and copy its contents to your clipboard.
     - Paste the file contents into the Glue script editor window. 
     - Click "Save" to save the job script.
     - Click "Run job" and expand the "Security configuration, script libraries, and job parameters" options on the run dialog.
     - At the bottom we will add two "Job parameters".
        --S3_JSON_INPUT_PATH = s3://personalize-data-224124347618/raw-events/events.json
        --S3_CSV_OUTPUT_PATH = s3://personalize-data-224124347618/transformed/
     - Click the "Run job" button to start the job. Logging output will start being displayed in the Logs tab as the job begins to run.
     - When the job completes, click the "X" in the upper right corner of page to exit the job script editor.


3. Use a Glue Crawler to crawl the output of the ETL job so it can be queried and visualized.

-  Browse to AWS Glue in the AWS console. Ensure that you are still in the N. Virginia region.
-  Click "Crawlers" in the left navigation.
- Click "Add crawler" to create a crawler.
- Enter a name for the crawler such as SegmentEventsCrawler and click "Next".
- For the datastore, select S3 and "Specified path in my account".
- For the "Include path", click the folder icon and select the "transformed" folder in the "personalize-data-..." bucket. Do NOT select the "run-..." file.
- Click "Next" and then "Next" again when prompted to add another data store.
- For the IAM role, select "Choose an existing IAM role" radio button and then select the "SegmentPersonalizeWorkship-GlueServiceRole-..." role from the dropdown.
- Click Next.
- Leave the Frequency set to "Run on demand" and click Next.
- For the crawler output, create a database called "segmentdata".
- Click Next.
- On the review page, click "Finish".
- From the Crawlers page, click the "Run it now?" link or select the crawler and click "Run crawler".
- Wait for the crawler to finish. It should take about 1-2 minutes.

## Data Exploration

1. Use Athena to query transformed data

- Browse to Athena in the AWS console. Ensure that you are still in the N. Virginia region.
- Make sure your database is selected in the left panel and you should see the "transformed" table below the database.
- Query the first 50 records from the CSV by copy/pasting the following query into the "New query" tab.
    SELECT * FROM "segmentdata2"."transformed" limit 50;
- Click "Run query" to execute the query. You should see results displayed.


## Create Dataset Group



## Upload Interactions Dataset