## Module 1 Answer 

## Docker & SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits* 

## Answer 1. Knowing docker tags

- [ ] `--delete`
- [ ] `--rc`
- [ ] `--rmc`
- [x] `--rm`


## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ). 

What is version of the package *wheel* ?

## Answer 2. Understanding docker first run 

- [x] 0.42.0
- [ ] 1.0.0
- [ ] 23.0.1
- [ ] 58.1.0


# Prepare Postgres

## Question 3. Count records 

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

## Answer 3. Count records 

`SELECT
    COUNT(1) AS "count"
FROM
   green_taxi_data  t
WHERE CAST(lpep_pickup_datetime AS DATE) = '2019-09-18' AND
    CAST(lpep_dropoff_datetime AS DATE) = '2019-09-18';`

- [ ] 15767
- [x] 15612
- [ ] 15859
- [ ] 89009

## Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance
Use the pick up time for your calculations.

## Answer 4. Largest trip for each day

`SELECT
	CAST(lpep_pickup_datetime AS DATE) as "start_date",
    MAX(trip_distance) as "maximum_distance"	
FROM
   green_taxi_data  t  
GROUP BY
	CAST(lpep_pickup_datetime AS DATE) 
ORDER BY
	"maximum_distance" desc
Limit 5;`

- [ ] 2019-09-18
- [ ] 2019-09-16
- [x] 2019-09-26
- [ ] 2019-09-21


## Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
 
## Answer 5. Three biggest pick up Boroughs

 `SELECT
    z."Borough",
    SUM(g.total_amount) AS total_amount_sum
FROM
    green_taxi_data g
JOIN 
	zones z on g."PULocationID" = z."LocationID"
WHERE
	CAST(lpep_pickup_datetime AS DATE) = '2019-09-18'
	AND z."Borough" <> 'Unknown'
GROUP BY
    z."Borough"
HAVING
	SUM(g.total_amount) > 50000
ORDER BY
    total_amount_sum DESC`

- [x] "Brooklyn" "Manhattan" "Queens"
- [ ] "Bronx" "Brooklyn" "Manhattan"
- [ ] "Bronx" "Manhattan" "Queens" 
- [ ] "Brooklyn" "Queens" "Staten Island"


## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`
## Answer 6. Largest tip

`select 
zd."Zone" as "dropped_zone",
MAX(g.tip_amount) as "largest_tip"
from
green_taxi_data g 
JOIN 
zones z on g."PULocationID" = z."LocationID"
JOIN 
zones zd on g."DOLocationID" = zd."LocationID"
where
CAST(g.lpep_pickup_datetime AS DATE) between '2019-09-01' and '2019-09-30'
AND z."Zone" = 'Astoria'
group by  zd."Zone"
order by "largest_tip" desc`

- [ ] Central Park
- [ ] Jamaica
- [x] JFK Airport
- [ ] Long Island City/Queens Plaza



## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Paste the output of this command into the homework submission form.

``

## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw01
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 29 January, 23:00 CET
