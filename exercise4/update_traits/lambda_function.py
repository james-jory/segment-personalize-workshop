import json
import boto3
import os
import base64
import requests  # Needed for Personas + Segment Events REST APIs
import json
import dateutil.parser as dp
import init_personalize_api as api_helper

personas_endpoint_url = "https://profiles.segment.com/v1/spaces"
connections_endpoint_url = "https://api.segment.io/v1"

personas_api_key = os.environ['personas_api_key']
personas_workspace_id = os.environ['personas_workspace_id']
connections_source_api_key = os.environ['connections_source_api_key']

def api_get(url, key):
    myResponse = requests.get(url,auth=(key, ''))
    if(myResponse.ok):
        jData = json.loads(myResponse.content)
        return jData
    else:
        myResponse.raise_for_status()

def api_post(url, key, payload):
    myResponse = requests.post(url,auth=(key, ''), json=payload)
    if(myResponse.ok):
        jData = json.loads(myResponse.content)
        return jData
    else:
        myResponse.raise_for_status()

def get_user_traits(user_id):
    # Calls Profile API to get the user profile traits by their userId
    formatted_url = "{:s}/{:s}/collections/users/profiles/user_id:{:s}/traits?limit=100".format(personas_endpoint_url, personas_workspace_id, user_id)
    jData = api_get(formatted_url, personas_api_key)
    return jData['traits'] # return the traits dict

def set_user_traits(user_id, traits):
    # Sends an identify call to Personas to update a user's traits
    formatted_url = "{:s}/identify".format(connections_endpoint_url)
    message = { "traits": traits, "userId": user_id, "type": "identify" }
    api_post(formatted_url, connections_source_api_key, message)

def lambda_handler(event, context):
    """
    """

    if not 'personalize_tracking_id' in os.environ:
        raise Exception('personalize_tracking_id not configured as environment variable')

    if not 'personalize_campaign_arn' in os.environ:
        raise Exception('personalize_campaign_arn not configured as environment variable')

    # Initialize Personalize API (this is temporarily needed until Personalize is fully
    api_helper.init()

    print("event: " + json.dumps(event))

    # Allow Personalize API to be overriden via environment variables. Optional.
    runtime_params = { 'service_name': 'personalize-runtime', 'region_name': 'us-east-1', 'endpoint_url': 'https://personalize-runtime.us-east-1.amazonaws.com' }
    if 'region_name' in os.environ:
        runtime_params['region_name'] = os.environ['region_name']
    if 'endpoint_url' in os.environ:
        runtime_params['endpoint_url'] = os.environ['endpoint_url']

    personalize_runtime = boto3.client(**runtime_params)
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
            print("Calling Personalize.Record()")
            userId = segment_event['userId']
            properties = { "id": segment_event["properties"]["sku"] }
            personalize_events.put_events(
                trackingId = os.environ['personalize_tracking_id'],
                userId = userId,
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

            params = { 'campaignArn': os.environ['personalize_campaign_arn'], 'userId': userId }

            response = personalize_runtime.get_recommendations(**params)

            recommended_items = [d['itemId'] for d in response['itemList'] if 'itemId' in d]

            userTraits = get_user_traits(userId)

            print(userTraits)

            if 'purchased_products' in userTraits:
                # Remove already purchased products from the recommended traits
                recommended_items = list(set(userTraits['purchased_products']).symmetric_difference(recommended_items))

            print(recommended_items)

            # Set the updated recommendations on the user's profile
            set_user_traits(userId, { 'recommended_products' : recommended_items })

        else:
            print("Segment event does not contain required fields (anonymousId, sku, and userId)")
