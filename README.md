# Solar Irradiance Eko Station Graphs

 
This package of scripts controls the function of pushing updated data extracted from the EKO station.

## Pre-Requisites
- Pandas
- Numpy 
- Plotly 
- Psycopg Binary 
- Postgres Database holding EKO station data.

## CRON JOBS

It is important to use cron jobs to regularly clean data - the isolated CSV folder can be a point of breaking
if more than one file is stored there, therefore it's recommended to wipe the directory clean every 24 hours. 

## Docker images

PostgreSQL 14 container is used to store EKO station data. 


HOW TO DELETE OLD ROWS - based on current date.
`DELETE FROM radiance WHERE "Timestamp" LIKE '%current_date%';`


## Expected Output, Graphs and Console Logs

[![visualize-Plotly-Example.png](https://i.postimg.cc/pV4YT9nF/visualize-Plotly-Example.png)](https://ibb.co/2sqcxM6)

-- VisualizePlotly Output

[![am1-5-Script-Output.png](https://i.postimg.cc/vB80YKTh/am1-5-Script-Output.png)](https://postimg.cc/2qJQT24L)

-- AM1.5 Script Output
