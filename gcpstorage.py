from google.resumable_media.requests import ResumableUpload
from google.auth.transport.requests import AuthorizedSession
from google.resumable_media import requests, common
from google.auth.transport import requests
import os
import json
from google.cloud import storage
from config import cwd
from google.auth import impersonated_credentials
from google.oauth2 import service_account

def gbucket(filename):
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
    
    client = storage.Client()
    client=client._credentials
    transport=AuthorizedSession(
            credentials=client)
    url_template = (
        u'https://www.googleapis.com/upload/storage/v1/b/{bucket}/o?'
        u'uploadType=resumable')

    upload_url = url_template.format(bucket='keelaa-images')
    chunk_size = 3 * 1024 * 1024
    upload = ResumableUpload(upload_url, chunk_size)
    print(upload.total_bytes is None,"klvnsdkfvnk")
    print(upload_url)
    stream = open(filename, u'rb')
    total_bytes = os.path.getsize(filename)
    metadata = {u'name': filename}
    response = upload.initiate(
        transport, stream, metadata, u'text/plain',
        total_bytes=total_bytes,stream_final=True)
    print(upload.total_bytes == total_bytes)
    return response
