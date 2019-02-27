import base64
import boto3
import json
import os
import dateutil.parser as dp
import init_personalize_api as api_helper

def lambda_handler(event, context):
    """ Consumes events from the Kinesis Stream destination configured in Segment.
    See the Segment documentation for how to setup Kinesis: https://segment.com/docs/destinations/amazon-kinesis/
    """

    if not 'personalize_tracking_id' in os.environ:
        raise Exception('personalize_tracking_id not configured as environment variable')

    # Initialize Personalize API (this is temporarily needed until Personalize is fully
    # integrated into boto3). Leverages Lambda Layer.
    api_helper.init()

    print("event: " + json.dumps(event))

    personalize_events = boto3.client('personalize-events')

    for record in event['Records']:
        print("Payload: " + json.dumps(record))
        segment_event = json.loads(base64.b64decode(record['kinesis']['data']).decode('utf-8'))
        print("Segment event: " + json.dumps(segment_event))

        # For the Personalize workshop, we really only care about these events
        supported_events = ['Product Added', 'Order Completed', 'Product Clicked']
        if ('anonymousId' in segment_event and
            'userId' in segment_event and
            'properties' in segment_event and
            'sku' in segment_event["properties"] and
            'event' in segment_event and
            segment_event['event'] in supported_events):
            print("Calling Personalize.put_events()")
            properties = { "id": segment_event["properties"]["sku"] }
            personalize_events.put_events(
                trackingId = os.environ['personalize_tracking_id'],
                userId = segment_event['userId'],
                sessionId = segment_event['anonymousId'],
                eventList = [
                    {
                        "eventId": segment_event['messageId'],
                        "sentAt": int(dp.parse(segment_event['timestamp']).strftime('%s')),
                        "eventType": segment_event['event'],
                        "properties": json.dumps(properties)
                    }
                ]
            )
        else:
            print("Segment event does not contain required fields (anonymousId, sku, and userId)")
