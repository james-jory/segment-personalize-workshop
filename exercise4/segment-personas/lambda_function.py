import json
import boto3
import os
import init_personalize_api as api_helper

def lambda_handler(event, context):
    """ Consumes events from the Kinesis Stream destination configured in Segment. 
    See the Segment documentation for how to setup Kinesis: https://segment.com/docs/destinations/amazon-kinesis/
    """

    # Initialize Personalize API (this is temporarily needed until Personalize is fully 
    # integrated into boto3). Leverages Lambda Layer.
    api_helper.init()
    
    print("event: " + json.dumps(event))

    api_params = { 'service_name': 'personalize-runtime', 'region_name': 'us-east-1', 'endpoint_url': 'https://personalize-runtime.us-east-1.amazonaws.com' }
    if 'region_name' in os.environ:
        api_params['region_name'] = os.environ['region_name']
    if 'endpoint_url' in os.environ:
        api_params['endpoint_url'] = os.environ['endpoint_url']

    personalize = boto3.client(**api_params)
    
    params = { 'campaignArn': 'arn:aws:personalize:us-east-1:224124347618:campaign/segment-campaign-e2e' }
    
    if 'userId' in event['queryStringParameters']:
        params['userId'] = event['queryStringParameters']['userId']
    if 'itemId' in event['queryStringParameters']:
        params['itemId'] = event['queryStringParameters']['itemId']
    if 'numResults' in event['queryStringParameters']:
        params['numResults'] = int(event['queryStringParameters']['numResults'])
    
    recommendations = personalize.get_recommendations(**params)

    print(recommendations)

    ''' 
    TODO:
    
    1. Call Segment Profile API to fetch customer profile.
    2. Filter recommendations from Personalize against purchase history attached to customer profile as trait.
    3. Make Segment identify call to update customer profile with filtered recommedations.
    4. Update return statement below to return filtered recommendations.
    '''

    return {
        'statusCode': 200,
        'body': json.dumps(recommendations)
    }
