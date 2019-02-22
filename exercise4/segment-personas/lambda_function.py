import json
import boto3
import os
import init_personalize_api as api_helper

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
