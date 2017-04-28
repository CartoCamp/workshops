-------------------------------------------
http://bit.ly/carto-camp-routing

## Welcome to Carto-Camp - Routing and Directions!

To follow along -
Set up a Google Api key here (you will need to be logged into your gmail account for this):
https://developers.google.com/maps/documentation/directions/get-api-key
This is for web-services -> directions API
Keep the tab open and the API key handy

Open your terminal and go to the place you want to set-up the environment (Desktop, Documents etc.)
Once there, do the following to grab the working folder into your system:

```
git clone https://github.com/CartoCamp/workshops.git
cd cd workshops/2017-04-28-carto-camp-routing
```
Once within the folder - we will now set up and activate our virtual environment so we do not have to worry about version dicrepancies!

Fire up your terminal and do the following:

```bash
cd carto-camp-routing
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

jupyter notebook
```
If this works, skip the next section

-----------------------------------------
If the `virtualenv` step fails, do this:

```
sudo pip install virtualenv
```
If you are with Anaconda and it fails - try the following:

```
conda update conda
conda install virtualenv
conda update virtualenv
virtualenv venv
```
If that doesn't work too for Anaconda do:

```
conda create -n venv
```
And follow from `source venv/bin/activate`

--------------------------------------------
### Starting with the main file:

Source: https://s3.amazonaws.com/tripdata/index.html

Download the main file here: https://www.dropbox.com/s/brrp4o0sxrm70yy/citibike_mar17.csv?dl=0
These are all the citibike trips for the month of March'17.
Upload that file into your CARTO account. We do this so we can perform custom SQL queries and use the file directly in Python.

< It may take a while - let's chat till then! :) >

Once it is in there - we will start working with the Ipython notebook within our environment called `Carto-Camp - Google Maps API and Routing.ipynb`

Open the file and let's start!

< All instructions for the Python functionality is within the notebook - so we can get off this tab for a bit - Phew!>

### Understanding the SQL query:

- 1. The first one used to select one random trip for one random day:

     Source: Chris Whong's [blog](http://chriswhong.com/data-visualization/taxitechblog1/) for his amazing project [NYC Taxis - A Day in the Life](http://chriswhong.github.io/nyctaxi/)
     And this [Reddit thread and contributor](https://www.reddit.com/r/bigquery/comments/28ialf/173_million_2013_nyc_taxi_rides_shared_on_bigquery/)
     
```
SELECT trip_data.cartodb_id, trip_data.bike_id, trip_data.start_time, trip_data.stop_time, trip_data.trip_duration, trip_data.start_station_name, trip_data.end_station_name, trip_data.start_station_latitude, trip_data.start_station_longitude, trip_data.end_station_latitude, trip_data.end_station_longitude 
FROM(
  SELECT bike_id, start_time, stop_time, start_station_name, end_station_name, trip_duration, cartodb_id, start_station_latitude, start_station_longitude, end_station_latitude, end_station_longitude FROM citibike_mar17 as a
  JOIN(SELECT unnest(Array[25818, 27054, 26541, 26785, 26405, 26354, 26742, 25597, 26478, 26920]) as oneid, Date(start_time) onedate
       FROM citibike_mar17
       ORDER BY RANDOM()
       LIMIT 1) b
  ON a.bike_id = b.oneid
  WHERE Date(start_time) = onedate
  ) as trip_data
ORDER BY trip_data.start_time ASC
```
  This query is joining the dataset by creating instances of it on `bike_id` and `date` by first selecting a random `bike_id` and `date`.
  
### Styling the data we got in CARTO:


[![carto-camp](https://cloud.githubusercontent.com/assets/14189245/25540228/582eb924-2c18-11e7-97ca-97a225584ab1.gif)](https://team.carto.com/u/mehak-carto/builder/584986d2-2bb9-11e7-afcc-0e05a8b3e3d7/embed)


Go to the `datasets` of your account and you will see the datasets already uploaded and ready to be used!

Select the `carto-camp-routing` dataset and `CREATE MAP` with it.

- 1. Analysis - `Connect with Lines`
- 2. Separate the source layer and put it on top
- 3. Style!

You can also `ADD` the `random_trip_stations` for context of which stations the bikes accessed!

### Hope this was useful and fun! :) - Questions?


