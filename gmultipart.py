from google.auth.transport.requests import AuthorizedSession
from google.auth.transport import requests
from google.resumable_media.requests import MultipartUpload
import os
import json
from google.cloud import storage
from config import cwd
from google.auth import impersonated_credentials
from google.oauth2 import service_account
import base64
import re


def gmulti(filename,name):
    storage.Client()
    target_scopes = ['https://www.googleapis.com/auth/devstorage.read_only']
    source_credentials = service_account.Credentials.from_service_account_file(
        cwd+"/keelaa.json",
        scopes=target_scopes,
        subject='keelaa-storage@keelaa-1535435701928.iam.gserviceaccount.com')
#    credentials=cwd+"/keelaa.json"
    target_credentials = impersonated_credentials.Credentials(
    source_credentials=source_credentials,
    target_principal='keelaa-storage@keelaa-1535435701928.iam.gserviceaccount.com',
    target_scopes=target_scopes,
    lifetime=500)
    credentials = service_account.Credentials.from_service_account_file(cwd+"/keelaa.json")
    name1=re.sub('\.[a-zA-Z]+','',name)
    client = storage.Client()
    client=client._credentials
    transport=AuthorizedSession(
            credentials=client)
    content_type = u'text/plain'
    
    with open(filename, "rb") as imageFile:
        data = imageFile.read()
    url_template = (
     u'https://www.googleapis.com/upload/storage/v1/b/{bucket}/o?'
     u'uploadType=multipart')
    upload_url = url_template.format(bucket='keelaa-images')
    upload = MultipartUpload(upload_url)
    metadata = {
     u'name': name1,
     u'metadata': {
         u'color': u'grurple',
        },
    }
    response = upload.transmit(transport, data, metadata, content_type)
    print(upload.finished)
    return response.json()