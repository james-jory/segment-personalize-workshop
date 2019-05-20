-- Demonstrates how to create a table in Athena that can be used
-- to query event data written to S3 by Segment's S3 destination.
-- This is helpful in exploring training data before being uploaded
-- into Personalize before model building. 
--
-- See https://segment.com/docs/destinations/amazon-s3/
--
-- Note that special handling is required to map JSON field names
-- for Segment traits that contain spaces to Athena-safe 
-- variants. Additional mappings may be required to support your
-- trait naming scheme. 
CREATE EXTERNAL TABLE IF NOT EXISTS segment_logs (
  anonymousId string,
  channel string,
  context struct<ip:string,
    library:struct<name:string, version:string>>,
  event string,
  messageId string,
  originalTimestamp string,
  projectId string,
  properties struct<browser:string,
    operating_system:string,
    page_name:string,
    sku:string>,
  traits struct<campaign_name:string,
    campaign_source:string,
    experiment_group:string,
    favorite_departments:string,
    invited_user:string,
    referrering_domain:string,
    browser:string,
    email:string,
    first_name:string,
    ip:string,
    last_name:string,
    lifetime_value:string,
    likelihood_to_buy:float,
    operating_system:string>,
  receivedAt string,
  sentAt string,
  `timestamp` string,
  type string,
  userId string,
  version INT,
  writeKey string
  )           
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  "mapping.campaign_name"="Campaign Name",
  "mapping.campaign_source"="Campaign Source",
  "mapping.experiment_group"="Experiment Group",
  "mapping.favorite_departments"="Favorite Departments",
  "mapping.invited_user"="Invited User?",
  "mapping.referrering_domain"="Referrering Domain"
  )
LOCATION 's3://segment-personalize-workshop/segment-logs/';