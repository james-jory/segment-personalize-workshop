import json
import boto3
import os
import requests  # Needed for Segment Events REST APIs
import dateutil.parser as dp
import init_personalize_api as api_helper # This is only needed for the Personalize beta

from botocore.exceptions import ClientError

connections_endpoint_url = "https://api.segment.io/v1"
connections_source_api_key = os.environ['connections_source_write_key']

def api_post(url, key, payload):
    myResponse = requests.post(url,auth=(key, ''), json=payload)
    if(myResponse.ok):
        jData = json.loads(myResponse.content)
        return jData
    else:
        myResponse.raise_for_status()

def set_user_traits(user_id, traits):
    # Sends an identify call to Personas to update a user's traits
    formatted_url = "{:s}/identify".format(connections_endpoint_url)
    message = { "traits": traits, "userId": user_id, "type": "identify" }
    try:
        response = api_post(formatted_url, connections_source_api_key, message)
    except HTTPError as error:
        status = error.response.status_code
        if status >= 400 and status < 500:
            print('Segment: 400 error, more than likely you sent an invalid request.')
        elif status >= 500:
            print('Segment: There was a server error on the Segment side.')

def lambda_handler(event, context):
    if not 'personalize_tracking_id' in os.environ:
        raise Exception('personalize_tracking_id not configured as environment variable')
    if not 'personalize_campaign_arn' in os.environ:
        raise Exception('personalize_campaign_arn not configured as environment variable')

    # Initialize Personalize API (this is temporarily needed until Personalize is fully
    # available in the boto APIs
    api_helper.init()

    print("Segment Event: " + json.dumps(event))

    # Allow Personalize API to be overriden via environment variables. Optional.
    runtime_params = { 'service_name': 'personalize-runtime',
                       'region_name': 'us-east-1',
                       'endpoint_url': 'https://personalize-runtime.us-east-1.amazonaws.com' }
    if 'region_name' in os.environ:
        runtime_params['region_name'] = os.environ['region_name']
    if 'endpoint_url' in os.environ:
        runtime_params['endpoint_url'] = os.environ['endpoint_url']

    personalize_runtime = boto3.client(**runtime_params)
    personalize_events = boto3.client(service_name='personalize-events')

    # Segment will invoke your function once per event type you have configured
    # in the Personalize destination

    try:
        if ('anonymousId' in event and
            'userId' in event and
            'properties' in event):
            print("Calling Personalize.Record()")
            userId = event['userId']

            # You will want to modify this part to match the event props
            # that come from your events - Personalize will want the sku or
            # item ids for what your users are browsing or purchasing
            properties = { "itemId": event["properties"]["sku"] }

            response = personalize_events.put_events(
                trackingId = os.environ['personalize_tracking_id'],
                userId = userId,
                sessionId = event['anonymousId'],
                eventList = [
                    {
                        "eventId": event['messageId'],
                        "sentAt": int(dp.parse(event['timestamp']).strftime('%s')),
                        "eventType": event['event'],
                        "properties": json.dumps(properties)
                    }
                ]
            )

            params = { 'campaignArn': os.environ['personalize_campaign_arn'], 'userId': userId }

            response = personalize_runtime.get_recommendations(**params)

            recommended_items = [d['itemId'] for d in response['itemList'] if 'itemId' in d]

            print(recommended_items)

            # Set the updated recommendations on the user's profile - note that
            # this user trait can be anything you want
            set_user_traits(userId, { 'recommended_products' : recommended_items })

        else:
            print("Segment event does not contain required fields (anonymousId, sku, and userId)")
    except ValueError as ve:
        print("Invalid JSON format received, check your event sources.")
    except KeyError as ke:
        print("Invalid configuration for Personalize, most likely.")
    except ClientError as ce:
        print("ClientError - most likely a boto3 issue.")
        print(ce.response['Error']['Code'])
        print(ce.response['Error']['Message'])
