import boto3
import os

from .env_variables import getVariable

def uploadImageUser(username, file_image, fileName):
    s3 = boto3.client('s3')

    output = os.path.join("/tmp/", fileName)
    with open(output, "wb") as file:
        file.write(file_image.read())

    s3BucketPath = getVariable('s3BucketPath')
    filePathS3 = username + '/' + fileName
    completePath = s3BucketPath + filePathS3
    s3.upload_file('/tmp/' + fileName, 'insta-project-photo-s3bucket', filePathS3)

    return completePath