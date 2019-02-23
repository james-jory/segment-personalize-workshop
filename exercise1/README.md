# Exercise 1 - Data Transformation, Filtering, and Exploration

## Overview

The ability of machine learning models to make effective recommendations is largely influenced by the quantity and quality of data input during the training process. For most personalization ML solutions, training data typically comes from clickstream data collected from websites, mobile applications, and other online & offline channels where end-users are interacting with items for which we wish to make recommendations. Examples of clickstream events include viewing items, adding items to a list or cart, and of course purchasing items. Although an Amazon Personalize Campaign can be started with just new clickstream data going forward, the initial quality of the recommendations will not be as high as a model that has been trained on a significant amount of historical data.

> There is a minimum amount of data that is necessary to train a model. Using existing historical data allows you to immediately start training a solution. If you ingest data as it is created, and there is no historical data, it can take a while before training can begin.

### What You'll Be Building

In this exercise we will walk through the process required to take the raw historical clickstream data collected by Segment to train a model in Amazon Personalize. The advantage of bootstrapping Personalize with historical clickstream data is that you will start with a model that has the benefit of past events to make more accurate recommendations. Segment provides the ability to push clickstream data to the following locations in your AWS account.

* S3 bucket
* Kinesis Data Stream
* Kinesis Data Firehose
* Redshift

For this exercise we will walk you through how to setup an S3 destination in your Segment account. In the interest of time, though, we will provide a pre-made test dataset that you will upload to S3 yourself. Then you will use AWS Glue to create an ETL (extract, transform, load) Job that will filter and transform the raw JSON file into the format required by Personalize. The output file will be written back to S3. Finally, you will learn how to use Amazon Athena to query and visualize the data in the transformed file directly from S3. 

### Exercise Preparation

If you haven't already cloned this repository to your local machine, do so now.

```bash
git clone https://github.com/james-jory/segment-personalize-workshop.git
```

## Part 1 - Create S3 Destination in Segment

TODO: write instructions and capture screenshots

Detailed instructions can be found on Segment's [documentation site](https://segment.com/docs/destinations/amazon-s3/).

## Part 2 - Upload Raw Interaction Test Data to S3

Upload the sample raw dataset to the S3 bucket which has been created for you in the AWS-provided workshop account. The S3 bucket name will be in the format `personalize-data-ACCOUNT_ID` where ACCOUNT_ID is the ID for the AWS account that you're using for the workshop.

1. Log in to the AWS console. If you are participating in an AWS led workshop, use the instructions provided to access your temporary workshop account.
2. Browse to the S3 service.
3. Click on the bucket with a name like `personalize-data-...`.
4. Create a folder called `raw-events` in this bucket.
5. Click on the `raw-events` folder just created.
6. Upload the file `data/raw-events/events.json.gz` to the `raw-events` folder.

> If you're stepping through this workshop in your own personal AWS account, you will need to create an S3 bucket yourself that has the [necessary bucket policy](https://docs.aws.amazon.com/personalize/latest/dg/data-prep-upload-s3.html) allowing Personalize access to your bucket. Alternatively, you can apply the CloudFormation template [eventengine/workshop.template](eventengine/workshop.template) within your account to have these resources created for you.

## Part 3 - Data Preparation

Since the raw format, fields, and event types in the Segment event data cannot be directly uploaded to Amazon Personalize for model training, this step will guide you through the process of transforming the data into the format expected by Personalize. We will start with raw event data that has already aggregated into a single JSON file which you uploaded to S3 in the previous step. We will use AWS Glue to create an ETL job that will take the JSON file, apply filtering and field mapping to each JSON event, and write the output back to S3 as a CSV file.

### Create AWS Glue ETL Job

First, ensure that you are logged in to the AWS account provided to you for this workshop. Then browse to the Glue service in the console, making sure that the AWS region is "N. Virginia" (us-east-1). Then click "Jobs" in the left navigation on the Glue console page.

![Glue Jobs](images/GlueJobs.png)

Click the "Add job" button and enter the following information.

* Enter a job name such as "SegmentEventsJsonToCsv".
* For IAM role, a role has already been created for you that starts with the name "SegmentPersonalizeWorkshop-GlueServiceRole-...". Select this role.
* Leave Type as "Spark".
* For "This job runs", click the radio button "A new script to be authored by you".
* Leave everything else the same and click Next at the bottom of the form.
* On the "Connections" step just click "Save job and edit script" since we are not accessing data in a database for this job.

The source code for the Glue job has already been written. Copy the contents of [etl/glue_etl.py](etl/glue_etl.py) to your clipboard and paste it into the Glue editor window. Click "Save" to save the job script.

![Glue Job Script](images/GlueEditJobScript.png)

Let's review the script in more detail.

TODO

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