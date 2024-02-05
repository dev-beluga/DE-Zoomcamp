import pyarrow as pa
import pyarrow.parquet as pq
import os
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# update the variables below
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/src/gcp-cred.json'
project_id = 'terrform-demo-412419'
bucket_name = 'terraform-ny-taxi-bucket'
object_key = 'ny_taxi_data.parquet'
table_name = 'nyc_taxi_data'
root_path = f'{bucket_name}/{table_name}'



@data_exporter
def export_data_to_google_cloud_storage(data: DataFrame, **kwargs) -> None:
    print(type(data))

    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    table = pa.Table.from_pandas(data)

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['lpep_pickup_date'],
        filesystem=gcs
    )
