import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

def upload_file(file):
    connection_string = os.getenv("BLOB_CONNECTION_STRING")
    container_name = os.getenv("CONTAINER_NAME")

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    blob_client = container_client.get_blob_client(file.filename)
    blob_client.upload_blob(file, overwrite=True)

    return blob_client.url