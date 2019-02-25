import json
import boto3
import os
import requests  # Needed for Personas + Segment Events REST APIs
import json
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
    """ Proxies requests from API Gateway to the Personalize GetRecommendations endpoint.
    This function also fetches the customer's profile from Segment and illustrates how to
    use a trait on the profile to perform filtering of recommendations. For example, to filter
    recommendatios for products that the customer has purcased since the model was last trained.

    This function accepts the following arguments as query string parameters:
    userId - ID of the user to make recommendations (required for recommendations for a user)
    itemId - ID of the item to make recommendations (i.e. related items) (required for related items)
    numResults - number of recommendations to return (optional, will inherit default from Personalize if absent)
    """

    # Initialize Personalize API (this is temporarily needed until Personalize is fully
    # integrated into boto3). Leverages Lambda Layer.
    api_helper.init()

    print("event: " + json.dumps(event))

    # Allow Personalize API to be overriden via environment variables. Optional.
    api_params = { 'service_name': 'personalize-runtime', 'region_name': 'us-east-1', 'endpoint_url': 'https://personalize-runtime.us-east-1.amazonaws.com' }
    if 'region_name' in os.environ:
        api_params['region_name'] = os.environ['region_name']
    if 'endpoint_url' in os.environ:
        api_params['endpoint_url'] = os.environ['endpoint_url']

    personalize = boto3.client(**api_params)

    # Build parameters for recommendations request. The Campaign ARN must be specified as
    # an environment variable.
    if not 'personalize_campaign_arn' in os.environ:
        return {
            'statusCode': 500,
            'body': 'Server is not configured correctly'
        }

    params = { 'campaignArn': os.environ['personalize_campaign_arn'] }

    if 'userId' in event['queryStringParameters']:
        params['userId'] = event['queryStringParameters']['userId']
    if 'itemId' in event['queryStringParameters']:
        params['itemId'] = event['queryStringParameters']['itemId']
    if 'numResults' in event['queryStringParameters']:
        params['numResults'] = int(event['queryStringParameters']['numResults'])

    recommendations = personalize.get_recommendations(**params)

    # For this version of the function we're just returning the recommendations from
    # Personalize directly back to the caller.
    print(recommendations)

    '''
    TODO:

    1. Call Segment Profile API to fetch customer profile.
    2. Filter recommendations from Personalize against purchase history attached to customer profile as trait.
    3. Update return statement below to return filtered recommendations.
    '''

    return {
        'statusCode': 200,
        'body': json.dumps(recommendations)
    }
