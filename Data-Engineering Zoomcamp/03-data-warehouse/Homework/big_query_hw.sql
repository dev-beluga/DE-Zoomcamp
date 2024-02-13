--Creating external table referring to gcs path

CREATE OR REPLACE EXTERNAL TABLE `terrform-demo-412419.ny_taxi.external_green_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://ny-green_taxi_bucket/ny_green_taxi_data-2022.parquet']);

--------------------------------------------------------------------------------
--Create table from external table

CREATE OR REPLACE TABLE terrform-demo-412419.ny_taxi.green_tripdata AS 
SELECT *, TIMESTAMP_MICROS(CAST(lpep_pickup_datetime / 1000 AS INT64)) AS cleaned_pickup_datetime, TIMESTAMP_MICROS(CAST(lpep_dropoff_datetime / 1000 AS INT64)) AS cleaned_dropoff_datetime FROM `terrform-demo-412419.ny_taxi.external_green_tripdata`;


-- SELECT TIMESTAMP_MICROS(CAST(lpep_dropoff_datetime / 1000 AS INT64)) AS cleaned_dropoff_datetime
-- FROM terrform-demo-412419.ny_taxi.external_green_tripdata;
--------------------------------------------------------------------------------

-- Question 1: What is count of records for the 2022 Green Taxi Data??

  select count(*) from terrform-demo-412419.ny_taxi.green_tripdata;

-- Question 2: Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.

  SELECT DISTINCT(pulocation_id) from terrform-demo-412419.ny_taxi.external_green_tripdata;

  SELECT DISTINCT(pulocation_id) from terrform-demo-412419.ny_taxi.green_tripdata;

-- Question 3. How many records have a fare_amount of 0?

  select count(*) from terrform-demo-412419.ny_taxi.green_tripdata 
  where fare_amount = 0;

  -- select * from terrform-demo-412419.ny_taxi.green_tripdata;

-- Question 4. What is the best strategy to make an optimized table in Big Query?
CREATE OR REPLACE TABLE terrform-demo-412419.ny_taxi.green_tripdata_partitoned_clustered
PARTITION BY DATE(cleaned_pickup_datetime)
CLUSTER BY pulocation_id AS
SELECT * FROM terrform-demo-412419.ny_taxi.green_tripdata ;


-- Question 5. What's the size of the tables?

SELECT DISTINCT(pulocation_id)
FROM terrform-demo-412419.ny_taxi.green_tripdata
WHERE cleaned_pickup_datetime BETWEEN TIMESTAMP('2022-06-01') AND TIMESTAMP('2022-06-30');


SELECT DISTINCT(pulocation_id)
FROM terrform-demo-412419.ny_taxi.green_tripdata_partitoned_clustered
WHERE cleaned_pickup_datetime BETWEEN '2022-06-01' AND '2022-06-30';


-- Question 8. Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

  select count(*) from terrform-demo-412419.ny_taxi.green_tripdata 

-- This query will process 0 B when run.
-- BigQuery does not scan actual data at all and rather uses metadata to just simply get count of rows , that's why it is saying 0 B.