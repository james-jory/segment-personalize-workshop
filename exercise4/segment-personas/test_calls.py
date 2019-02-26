import requests  # Needed for Personas + Segment Events REST APIs
import json
import boto3

personas_endpoint_url = "https://profiles.segment.com/v1/spaces"
connections_endpoint_url = "https://api.segment.io/v1"

personas_api_key = 'Rpn703c-OOJKr5gDTuou7ViQlroTxOgre_6OfChK_unKQalwpw-imDRZQivLq8sKjC2M0ngckQfLAM6KMAy5QckDPWOuhMxJC0H5Ymu4B-3HpePBgrkHmneSgchdG1LfRgcLJQZlcJYpaDXrPGDXUKdcuUUmJjDS-cht9Y-3SNf7O0uqyx7dPRbUzzVzzCiSuC4F4stVdt-6'
personas_workspace_id = 'DghtLzq1cc'
connections_source_api_key = 'SKDzoDFy36OqLdnV1dttMTsmKNrjY9TA'
campaign_arn = 'arn:aws:personalize:us-west-2:816059824474:campaign/flashgear-recs'

def api_get(url, key):
    myResponse = requests.get(url,auth=(key, ''))
    #print (myResponse.status_code)

    # For successful API call, response code will be 200 (OK)
    if(myResponse.ok):

        # Loading the response data into a dict variable
        # json.loads takes in only binary or string variables so using content to fetch binary content
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
        jData = json.loads(myResponse.content)
        print("GET reponse: {:s}".format(myResponse.text))
        return jData
    else:
      # If response code is not ok (200), print the resulting http error code with description
        myResponse.raise_for_status()

def api_post(url, key, payload):
    myResponse = requests.post(url,auth=(key, ''), json=payload)
    #print (myResponse.status_code)

    # For successful API call, response code will be 200 (OK)
    if(myResponse.ok):

        # Loading the response data into a dict variable
        # json.loads takes in only binary or string variables so using content to fetch binary content
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
        jData = json.loads(myResponse.content)
        return jData
    else:
      # If response code is not ok (200), print the resulting http error code with description
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
    print(json.dumps(message))
    api_post(formatted_url, connections_source_api_key, message)

test_user_id = '6378468709'
api_params = { 'service_name': 'personalize-runtime', 'region_name': 'us-west-2', 'endpoint_url': 'https://personalize-runtime.us-west-2.amazonaws.com' }
personalize = boto3.client(**api_params)
params = { 'campaignArn': campaign_arn, 'userId': test_user_id }

response = personalize.get_recommendations(**params)
#print(response['itemList'])

recommended_items = [d['itemId'] for d in response['itemList'] if 'itemId' in d]

print(recommended_items)

user_traits = get_user_traits(test_user_id)  # Get Brian Butler's traits

print(user_traits)

if 'purchased_products' in user_traits:
    # Remove already purchased products from the recommended traits
    recommended_items = list(set(user_traits['purchased_products']).symmetric_difference(recommended_items))

print(recommended_items)

set_user_traits(test_user_id, { 'recommended_products' : recommended_items })
