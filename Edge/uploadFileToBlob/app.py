import os
from dotenv import load_dotenv
from azure.storage.blob import BlobClient

load_dotenv()
BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")

parent = "Log"
# parent = "Report"

path = f"./{parent}/"

# file_name = "20230313-140020.csv"
file_name = "L20230301.log"

blob = BlobClient.from_connection_string(conn_str = BLOB_CONNECTION_STRING, container_name = BLOB_CONTAINER_NAME, blob_name = f"{parent}/" + file_name)
with open(f"{path}{file_name}", "rb") as data:
    try:
        blob_client = blob.upload_blob(data, overwrite=True)
        print(f"blob_client: {blob_client}")
    except Exception as ex:
        print(f"Exception: {ex}")