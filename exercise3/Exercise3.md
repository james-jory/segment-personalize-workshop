# Exercise 3 - Real-Time Data Collection & Recommendation Optimization

1. Create Kinesis Stream
    - Browse to Kinesis in the AWS console. Ensure that you are in the N. Virginia region.
    - Click "Get started" and then "Create data stream"
    - For the name of your stream, enter "SegmentDestinationStream" (required).
    - Enter 1 for the number of shards.
    - Click "Create Kinesis stream"

2. Create Kinesis destination in Segment to send events

    - Log in to Segment account.
    - Configure a Source in Segment. For example, a website Javascript or server Node.js source.
    - Configure a Kinesis Destination for the newly created Source.
        - For the AWS Kinesis Stream Region, enter us-east-1 and click Save.
        - For the Role Address you will need to find and copy the IAM role ARN to your clipboard
            - In another browser tab/window, login to your AWS account and browse to IAM.
            - Click on Roles in the left navigation.
            - Find the Role with a name that starts with "SegmentPersonalizeWorkshop-SegmentKinesisRole-...".
            - Click on the role name to view the role details.
            - At the top of the page where the "Role ARN" is displayed, click on the copy icon at the end of the line.
            - Switching back to your Segment tab/window, paste the Role ARN into the Role Address field and click Save.
        - For the Secret ID, enter "123456789" and click Save.
        - For the AWS Kinesis Stream Name, enter "SegmentDestinationStream" and click Save.
        - Activate the destination by clicking on the selector at the top of the page.

3. Send test events to Destination to verify configuration.

    - On the Kinesis configuration page in Segment, click on "Event Tester".
    - Under the Event Tester settings, click "Event Builder".
    - Set the Call Type to "Track" and event type to "Product Clicked".
    - Under Properties, create or change an existing property of key "sku" and value "ocean-blue-shirt".
    - Click "Send Event".
    - Change the sku and/or User ID and click Send Event again. Do this a few more times.

