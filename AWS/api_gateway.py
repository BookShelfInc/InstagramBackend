import requests
import json

from .env_variables import getVariable

def cropImage(image):
    API_ENDPOINT = getVariable('API_GATEWAY_IMAGE')

    data = {'bucket': getVariable('s3BucketName'), 'image': image}
    headers = {'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*'}

    r = requests.post(API_ENDPOINT, data=json.dumps(data), headers=headers)

    return r.text