# Personalize Workshop Exercise 4

## Exercise 4 - Activating Recommendations using Segment Personas
## **Overview**

After you create a campaign using Amazon Personalize, you are able to get two different types of recommendations, dependent on what recipe type was used to train the model.
For user-personalization and related-items recipes, the [GetRecommendations](https://docs.aws.amazon.com/personalize/latest/dg/API_RS_GetRecommendations.html) API returns a list of recommended items. For example, products or content can be recommended for users signed in to your website.

For search-personalization recipes, the [PersonalizeRanking](https://docs.aws.amazon.com/personalize/latest/dg/API_RS_PersonalizeRanking.html) API re-ranks a list of recommended items based on a specified query.

In this workshop we have been focused on building a user-personalization solution, trained on historical and real-time clickstream event data from Segment. In this final exercise we will pull together the foundation we built in [Exercise 1](https://github.com/james-jory/segment-personalize-workshop/blob/master/exercise1) to transform raw event data from Segment that we used to build a Personalize Solution and Campaign in [Exercise 2](https://github.com/james-jory/segment-personalize-workshop/blob/master/exercise2).

In [Exercise 3](https://github.com/james-jory/segment-personalize-workshop/blob/master/exercise3) we learned how to feed real-time event data from Segment into Personalize to improve the quality of recommendations. Now we will look at how to incorporate recommendations from Personalize into our application.

**What You'll Be Building**
We will start by building an API Gateway endpoint that calls a Lambda function to fetch recommendations from Personalize.  This example will show how to build a basic API endpoint to call Personalize directly from your applications for use cases where you will want to directly get recommendations.

Then we will return to the Lambda function we built in [Exercise 3](https://github.com/james-jory/segment-personalize-workshop/blob/master/exercise3) and enhance it to demonstrate how we can use Personas to activate recommendations from Personalize across other integrated applications in your Segment workspace (such as email marketing tools, analytics tools, and other advertising channels).

**Exercise Preparation**
If you haven't already cloned this repository to your local machine, do so now.

    git clone https://github.com/james-jory/segment-personalize-workshop.git
## **Part 1 - Create API Endpoint & Lambda Function**
![Exercise 4 Part 1 Architecture](https://github.com/james-jory/segment-personalize-workshop/raw/master/exercise4/images/Architecture-Exercise4-Part1.png)


First we will create a Lambda function that will be called by an API Gateway endpoint. In the AWS console for the account you've been assigned for the workshop, browse to the Lambda service page. Click the "Create function" button to create a new function.

![Lambda Create Function](https://github.com/james-jory/segment-personalize-workshop/raw/master/exercise4/images/LambdaCreateFunction.png)


Enter a name for your function, specify Python 3.7 as the runtime, and select the same IAM role we used for our Kinesis handler function (`module-personalize-SegmentKinesisHandlerRole-...`). Click "Create function".

![Lambda Function Config](https://github.com/james-jory/segment-personalize-workshop/raw/master/exercise4/images/LambdaRecEndpointCreate.png)


Scroll down to the "Function code" panel. The source code for the function has already been written and is provided in this repository at [recommendations/lambda_function.py](https://github.com/james-jory/segment-personalize-workshop/blob/master/exercise4/recommendations/lambda_function.py). Open this file in a new browser tab/window, copy it to your clipboard, and paste it into the source code editor for our Lambda function as show below. Click the "Save" button at the top of the page when you're done.

![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551204471385_image.png)


Next we need to register the Lambda Layer to wire up the Personalize API with the Python SDK like we did for our previous function. Click on "Layers" below the function name in the Lambda Designer panel. Then click the "Add a layer" button.

![Lambda Layer](https://github.com/james-jory/segment-personalize-workshop/raw/master/exercise4/images/LambdaRecAddLayer.png)


Select the Layer and latest version and click the "Add" button.

![Lambda Layer Select](https://github.com/james-jory/segment-personalize-workshop/raw/master/exercise4/images/LambdaAddLayerSelect.png)


Next, select "API Gateway" in the "Add triggers" panel in the Designer panel.

![Lambda API Gateway Trigger](https://github.com/james-jory/segment-personalize-workshop/raw/master/exercise4/images/LambdaRecAPIGW_Trigger.png)


Scroll down to the "Configure triggers" panel. For the API dropdown, select "Create a new API" and set the Security as "Open". For a production deployment you would want to [control access](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-control-access-to-api.html) to this endpoint but that is beyond the scope of this exercise. Click "Add" to add API Gateway as a trigger to our function and then click "Save" at the top of the page.

![Lambda API Gateway Config](https://github.com/james-jory/segment-personalize-workshop/raw/master/exercise4/images/LambdaRecAPIGW_Config.png)


Next, we need to add environment variables for Segment and for the function to tell it the Personalize Campaign to call for retrieving recommendations.

To obtain the Personalize Campaign ARN, browse to the Personalize service landing page in the AWS console. Select the Dataset Group you created earlier and then Campaigns in the left navigation. Click on the "segment-workshop-campaign" you created earlier and copy the "Campaign arn" to your clipboard.

![Personalize Campaign ARN](https://github.com/james-jory/segment-personalize-workshop/raw/master/exercise4/images/PersonalizeCampaignArn.png)


Return to our Lambda function and scroll down to the "Environment variables" panel. Add an environment variable with the key `personalize_campaign_arn` and value of the Campaign ARN in your clipboard. Scroll to the top of the page and click the "Save" button to save your changes.

![Lambda Campaign ARN Environment Variable](https://github.com/james-jory/segment-personalize-workshop/raw/master/exercise4/images/LambdaRecCampaignArn.png)


Now let's browse to the API Gateway service page in the AWS console to test our endpoint. Under "APIs" you should see the recommendations API created when we setup our Lambda trigger. Click on the API name.

![API Gateway APIs](https://github.com/james-jory/segment-personalize-workshop/raw/master/exercise4/images/APIGW_endpoint.png)


Click on the "Test" link to build a test request.

![API Gateway Test](https://github.com/james-jory/segment-personalize-workshop/raw/master/exercise4/images/APIGW_Test.png)


Select "GET" as the Method and enter a Query String of `userId=2941404340`. This is one of the users in our test dataset. Scroll to the bottom of the page and click the "Test" button.

![API Gateway Test](https://github.com/james-jory/segment-personalize-workshop/raw/master/exercise4/images/APIGW_TestGet.png)


This will send a request through API Gateway which will call our Lambda function. The function will query Personalize for recommendations and return the results to API Gateway.

![API Gateway Test](https://github.com/james-jory/segment-personalize-workshop/raw/master/exercise4/images/APIGW_TestGetResults.png)


This API framework and function provides the foundation for enhancing our function to filter recommendations based on recent purchase history in Segment.

## Part 2 - Filtering Recommendations using Customer Profile Traits

For this final step, you will configure Personas real-time computed traits, and then we will deploy a lambda function that uses that trait to synchronize recommended products with the user’s profile as they interact with your applications.  

This example will allow Personas to update a user trait for each user that completes an order via the Order Completed event.  So let’s set up that trait first.

Click the Personas Orb.

![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551194485012_image.png)


Then select ‘Computed Traits’.

![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551194585193_image.png)


Then click ‘Create Computed Trait’.


![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551194594333_image.png)


Select ‘Unique List.’  This will allow us to compute a list of unique skus from an Order Completed event.


![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551194599821_image.png)



![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551194605292_image.png)


Select the ‘Order Completed’ event in the ‘Select Event..’ dropdown

![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551194610863_image.png)


Then, select the ‘sku’ event property, and then click the ‘Preview’ button.  

Do not select a Time Frame for this trait!  Doing so will disable real-time computation.


![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551194620736_image.png)


This will generate a list of users that have completed orders, and their traits.

![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551194625799_image.png)


Skip this next step by clicking ‘Review & Create’

![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551194631795_image.png)


On this screen, name your trait ‘purchased_products’.  This will be used in the lambda you deploy to push recommendations to user profiles, so it must match this string or you have to update the lambda code.  Click ‘Create Computed Trait’.

![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551194636961_image.png)


This trait will now be computed for all users that interact with your Segment instance.

**Deploying Your Lambda**

In this step, you will deploy a lambda that takes events from Kinesis and updates user traits based on recommendations from the Personalize solution you deployed in earlier exercises.  We are going to use the Lambda you deployed in Exercise 3.

Go to your Lambdas list and click on the `SegmentDestinationHandler` Lambda you created earlier.


![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551249587393_image.png)


You will update the code in this Lambda with a new function, deployed via a .ZIP deployment package in the `exercise4/update-traits/function.zip` file.  To add the file, select the ‘Upload a .ZIP file’ option in the Function Code section of the configuration screen for SegmentDestinationHandler:


![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551249784480_image.png)


Your Lambda code should look something like this after this step:


![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551250573134_image.png)


Next, let’s update the environment variables this lambda will need to work properly.

First, we need the Personas API Key.  Open a new browser tab, and go to your Segment workspace. Click on Personas Orb > Settings > API Access tabs.  

Click the Generate button to generate an API key.


![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551194654728_image.png)


Name your key something like ‘personalize_workshop_key’

![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551194660016_image.png)


On the next screen, copy the API key to the clipboard.  This is only shown once so make sure you have it for the next step.

![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551194665767_image.png)


Click back to your Lambda browser tab or window, and paste the Personas API key under ‘personas_api_key’ in the Environment Variables section of the Lambda config screen.


![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551205490889_image.png)


Now let’s add the workspace ID.  Go back to your your Segment workspace tab or browser window, and click on the gear icon in the lower left corner:


![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551194676268_image.png)


Back to your Lambda browser tab or window and paste your workspace ID into a variable called ‘personas_workspace_id’:

![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551205490889_image.png)


And finally, we need a key for the Segment source that will get our update events.  Go back to your Segment workspace tab or window, and click on ‘personas-event-source’ and copy the write key from the Overview tab.


![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551194686388_image.png)


Back again to your Lambda tab or window, and paste the key under a property called ‘connections_source_api_key’:


![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551205490889_image.png)


*Make sure to click ‘SAVE’* here or you will need to do this again.

As events start to flow through Segment, you should start to see a list of recommended products from your Personalize solution appearing as traits on user Profiles in Personas.  To see user traits, go to your Segment workspace and click the Personas Orb > Explorer tab.  Click on a user profile as shown below.  Under Computed Traits should be your `purchased_products` trait.


![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551194671134_image.png)


And under Custom traits you will see a `recommended_products` trait, which is kept updated by your Lambda.


![](https://d2mxuefqeaa7sj.cloudfront.net/s_12A58A92405C56E8DE968E6DE63B3BFED1BB822EB344A5A338801C8B717BCDEB_1551194691333_image.png)

##
