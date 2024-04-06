import io
import os
import requests
import pandas as pd
from google.cloud import storage

"""
Pre-reqs: 
1. `pip install pandas pyarrow google-cloud-storage`
2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
3. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""

# services = ['fhv','green','yellow']
# https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-01.parquet
init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv'
# init_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/'
# switch out the bucketname

BUCKET = os.environ.get("GCP_GCS_BUCKET", "terraform-ny-taxi-bucket")


def upload_to_gcs(bucket_name, object_name, local_file):
    """Uploads a local file to Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

def web_to_gcs(year, service, bucket_name):
    """Downloads Parquet files from a web service and uploads them to Google Cloud Storage."""
    for i in range(12):
        # Format month with leading zero if needed
        month = f"{i+1:02d}"
        
        # Parquet file name
        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"

        # Download the Parquet file
        request_url = f"{init_url}{service}/{file_name}"
        headers = {'Accept-Encoding': 'gzip'}  # Add gzip header
        try:
            
            r = requests.get(request_url)
            with open(file_name, 'wb') as f:
                f.write(r.content)
            print(f"Downloaded: {file_name}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download: {e}")
            
        # Upload the Parquet file to Google Cloud Storage
        upload_to_gcs(bucket_name, f"{service}/{file_name}", file_name)
        print(f"Uploaded to GCS: {service}/{file_name}")

# Example usage
web_to_gcs('2019', 'fvh', 'terraform-ny-taxi-bucket')
# web_to_gcs('2019', 'yellow')
# web_to_gcs('2020', 'yellow')

