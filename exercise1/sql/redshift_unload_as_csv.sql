-- Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
-- SPDX-License-Identifier: MIT-0

-- Example query for unloading data from Redshift to a 
-- CSV file on S3 that is in the format expected by 
-- Amazon Personalize. Replace the values below with 
-- the AWS S3 bucket, credentials, and region appropriate
-- for your configuration.
UNLOAD ('
  SELECT
    user_id AS USER_ID,
    products_sku AS ITEM_ID,
    event AS EVENT_TYPE,
    date_part(epoch,"timestamp") AS TIMESTAMP
  FROM prod.order_completed
  UNION
  SELECT
    user_id AS USER_ID,
    products_sku AS ITEM_ID,
    event AS EVENT_TYPE,
    date_part(epoch,"timestamp") AS TIMESTAMP
  FROM prod.product_added
  UNION
  SELECT
    user_id AS USER_ID,
    products_sku AS ITEM_ID,
    event AS EVENT_TYPE,
    date_part(epoch,"timestamp") AS TIMESTAMP
  FROM prod.product_viewed
')
TO 's3://mybucket/my_folder'
CREDENTIALS 'aws_access_key_id=AWS_ACCESS_KEY_ID;aws_secret_access_key=AWS_SECRET_ACCESS_KEY;token=AWS_SESSION_TOKEN'
HEADER
REGION AS '<your-region>'
DELIMITER AS ','
PARALLEL OFF;