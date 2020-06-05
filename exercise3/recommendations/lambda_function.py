# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """ Proxies requests from API Gateway to the Personalize GetRecommendations endpoint. 
    This function provides the interception point that we need to perform real-time filtering 
    of recommendations based on traits on the customer's profile in Segment. Subsequent 
    iterations of this function developed as part of this exercise will incrementally add 
    this functionality.

    This function accepts the following arguments as query string parameters:
    userId - ID of the user to make recommendations (required for recommendations for a user)
    itemId - ID of the item to make recommendations (i.e. related items) (required for related items)
    numResults - number of recommendations to return (optional, will inherit default from Personalize if absent)
    """
    
    logger.info("event: " + json.dumps(event))

    # Allow Personalize region to be overriden via environment variable. Optional.
    api_params = { 'service_name': 'personalize-runtime' }
    if 'region_name' in os.environ:
        api_params['region_name'] = os.environ['region_name']

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
    logger.info(recommendations)

    return {
        'statusCode': 200,
        'body': json.dumps(recommendations)
    }
