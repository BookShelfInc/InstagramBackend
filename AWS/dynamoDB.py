import requests
import json

from .env_variables import getVariable

def postComment(commentId, comment, userId, photoId, toUserId):
    API_ENDPOINT = getVariable('API_GATEWAY_DYNAMODB')

    data = {
        "commentId": commentId,
        "userId": userId,
        "comment": comment,
        "photoId": photoId,
        "toUserId": toUserId
    }
    headers = {'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*'}

    r = requests.post(API_ENDPOINT, data=json.dumps(data), headers=headers)

    return r.text

def getNotifications(userId):
    API_ENDPOINT = getVariable('API_GATEWAY_DYNAMODB')+'/'+str(userId)

    headers = {'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*'}

    r = requests.get(API_ENDPOINT, headers=headers)

    return r.json()['Items']