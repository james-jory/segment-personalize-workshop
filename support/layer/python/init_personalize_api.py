import os

def init():
    """ Initializes the AWS API data path to include the models for the Personalize endpoints.
    To install this script as a Lambda layer, zip this file and all subdirectories and upload 
    them as a Lambda layer (using AWS console or CLI).
    This is only temporary until the Personalize SDK is fully integrated in boto3.
    """         
    dir_path = os.path.dirname(os.path.realpath(__file__))
    #print(dir_path)
    models_path = os.path.join(dir_path, 'models')
    #print(models_path)
    
    aws_data_path = set(os.environ.get('AWS_DATA_PATH', '').split(os.pathsep))
    aws_data_path.add(models_path)
    
    os.environ.update({
        'AWS_DATA_PATH': os.pathsep.join(aws_data_path)
    })
    #print(os.environ['AWS_DATA_PATH'])
    return 1