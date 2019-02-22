# Workshop Support Components

## Personalize API for boto3 (Preview)

Before you can call Personalize APIs from Python Lambda functions, the Personalize API model files have to be installed in the AWS SDK for Python. Rather than duplicate the bundling of the model files and initialization code for each function used in this workshop, a Lambda Layer is used to package the files and initialization code. Once uploaded as a Layer, the initialization helper function can be imported and called with a single line of code.