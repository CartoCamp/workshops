# Explore Time and Space with SQL and PostGIS

## Get this doc here: http://bit.ly/sql-postgis-time-space

## Get a free CARTO account

We're going to use CARTO's builder. Signup for free accounts here: https://carto.com/signup

**We're going to explore the space (through [PostGIS](http://postgis.net/)) and time ([native PostgreSQL](https://www.postgresql.org/docs/9.5/static/functions-datetime.html)) in today's workshops using two datasets that have lat/long and timestamps.**

## Spencer the Cat

![spencer_the_cat](http://cartodb.github.io/training/img/harvard/spencer.jpg)

Inspired by Andrew Hill

### Teaching the basics with Spencer

* Investigate Spencer's goings ons
  * general 'path' as reported by GPS
  * day of the week behavior
  * estimate velocity upper bound
* Look at the housing footprints to try to understand where Spencer lives

### Import Spencer's data

Import the data into your CARTO account:
https://dl.dropboxusercontent.com/u/1307405/CartoDB/spencer_the_cat.geojson

Make sure the table is named `spencer_the_cat`.

### Play around with the data


### What's Spencer doing on a Monday?

`'dow'` means 'day of the week'. The values will be from 0 to 6 (Sunday to Saturday).

```sql
SELECT *, date_part('dow', timestamp) as dow
FROM spencer_the_cat
WHERE date_part('dow', timestamp) = 1
```

### Let's look at paths by day of the week

Connect points with [`ST_MakeLine`](http://cartodb.github.io/training/img/harvard/spencer.jpg)

```sql
SELECT
  ST_Transform(
    ST_MakeLine(the_geom ORDER BY timestamp),
    3857) As the_geom_webmercator,
    min(cartodb_id) As cartodb_id
FROM spencer_the_cat
WHERE date_part('dow', timestamp) = 1
```

### Different days of the week

```sql
SELECT
  ST_Transform(
    ST_MakeLine(the_geom ORDER BY timestamp),
    3857) As the_geom_webmercator,
    min(cartodb_id) As cartodb_id,
  date_part('dow', timestamp)
FROM spencer_the_cat
GROUP BY date_part('dow', timestamp)
```


### Where is Spencer _fast_?

We can use the change in place (our `dx`) and change in time (`dt`) to find the upper bound for the speed of little spencer:

```sql
with cte as (
SELECT
  timestamp,
  EXTRACT(epoch FROM (timestamp - lag(timestamp, 1) OVER (ORDER BY timestamp asc))) as time_diff,
  ST_Distance(
    the_geom::geography,
    (lag(the_geom::geography, 1) OVER (ORDER BY timestamp asc))) as dist, the_geom, cartodb_id, the_geom_webmercator
  FROM spencer_the_cat
ORDER BY timestamp asc)

SELECT dist / time_diff as velocity, cartodb_id, the_geom, the_geom_webmercator
FROM cte
```

### Which house does Spencer probably live in?

To guess this, we might want to use the outlines of houses to look for the number of times Spencer intersected a house. We can import that data from here:

```text
http://andrew.cartodb.com/api/v2/sql?q=SELECT%20*%20FROM%20cambridge_buildings%20ORDER%20BY%20the_geom%20%3C-%3E%20CDB_LatLng(42.374444,%20-71.116944)%20LIMIT%2010&format=geojson&filename=spencer_houses
```

The data's originally from MassGIS's [Building Structures dataset](http://www.mass.gov/anf/research-and-tech/it-serv-and-support/application-serv/office-of-geographic-information-massgis/datalayers/ftpstructures.html).

To find out the number of house 'touches' Spencer has, let's first add a new column to store that information.

```sql
UPDATE structures_poly_9
SET n_spencer =
  (SELECT count(*)
   FROM spencer_the_cat
  WHERE ST_Intersects(the_geom, structures_poly_9.the_geom))
```

Let's turn the building to their centroids, and then visualize by the number of touches:

```sql
SELECT
  ST_Centroid(the_geom_webmercator) As the_geom_webmercator,
  n_spencer,
  cartodb_id
FROM
  structures_poly_9
```

![](http://i.imgur.com/ylOyKmr.png)

## Yellow Taxi Origin/Destination

This dataset of taxi trips (origin/destination pairs) for all trips from Aug 21, 2015 at 4 a.m. to 24 hours later.

Copy this link and import into your account:

```text
http://eschbacher.cartodb.com/api/v2/sql?q=SELECT%20*%20from%20taxi_aug_21_22_2015&format=csv&filename=taxi_aug_21_22_2015
```

The [Data dictionary](http://www.nyc.gov/html/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf) for this data is hosted on [TLC's website](http://www.nyc.gov/html/tlc/html/home/home.shtml).

## Origin/Destination

Let's look at 100 of the trips:

```sql
SELECT
  ST_Transform(
    ST_MakeLine(
      CDB_LatLng(pickup_latitude, pickup_longitude),
      CDB_LatLng(dropoff_latitude, dropoff_longitude)),
    3857) As the_geom_webmercator,
  cartodb_id
FROM
  taxi_aug_21_22_2015
LIMIT 100
```

![](http://i.imgur.com/wRbbjLw.png)

### Pickups or Dropoffs very near Goldman Sachs (200 West St.)

200 West Street is at lat/long `(40.7146153, -74.0145634)`. Let's look at 'em on Google Maps: https://www.google.com/maps/place/200+West+St,+New+York,+NY+10282/@40.7147361,-74.0142254,198m/data=!3m1!1e3!4m5!3m4!1s0x89c25a1b940ac987:0x4c3ca37c6872f351!8m2!3d40.7148895!4d-74.0143717

```sql
SELECT
  ST_Transform(
    ST_MakeLine(
      CDB_LatLng(pickup_latitude, pickup_longitude),
      CDB_LatLng(dropoff_latitude, dropoff_longitude)),
    3857) As the_geom_webmercator,
  cartodb_id
FROM
  taxi_aug_21_22_2015 As t,
  (SELECT ST_Transform(ST_Buffer(CDB_LatLng(40.7146153,-74.0145634)::geography, 50)::geometry, 4326) As the_geom) As gs
WHERE
  ST_Intersects(CDB_LatLng(pickup_latitude, pickup_longitude), gs.the_geom)
 OR
  ST_Intersects(CDB_LatLng(dropoff_latitude, dropoff_longitude), gs.the_geom)
```

### Morning arrivals at Goldman Sachs

Let's look at arrivals/departures from 8 a.m. to 10 a.m., and see where they come from.

```sql
SELECT
  ST_Transform(
    ST_MakeLine(
      CDB_LatLng(pickup_latitude, pickup_longitude),
      CDB_LatLng(dropoff_latitude, dropoff_longitude)),
    3857) As the_geom_webmercator,
  cartodb_id
FROM
  taxi_aug_21_22_2015 As t,
  (SELECT the_geom FROM ny_boroughs WHERE boroname = 'Manhattan') As mnhtn,
  (SELECT ST_Transform(ST_Buffer(CDB_LatLng(40.7146153,-74.0145634)::geography, 75)::geometry, 4326) As the_geom) As gs
WHERE
  (ST_Intersects(CDB_LatLng(pickup_latitude, pickup_longitude), gs.the_geom)
   OR
   ST_Intersects(CDB_LatLng(dropoff_latitude, dropoff_longitude), gs.the_geom)
  )
  AND
   tpep_pickup_datetime >= ('2015-08-21T08:00:00') AND
   tpep_pickup_datetime <= ('2015-08-21T10:00:00')
```

### Let's look at the number of pickups/dropoffs each hour of the day

How many at a time of the day?

```sql
SELECT
  ST_Transform(
    ST_MakeLine(
      CDB_LatLng(pickup_latitude, pickup_longitude),
      CDB_LatLng(dropoff_latitude, dropoff_longitude)),
    3857) As the_geom_webmercator,
  cartodb_id,
  count(*) OVER (PARTITION BY date_part('hour', tpep_pickup_datetime)),
  date_part('hour', tpep_pickup_datetime) as hour_of_day
FROM
  taxi_aug_21_22_2015 As t,
  (SELECT the_geom FROM ny_boroughs WHERE boroname = 'Manhattan') As mnhtn,
  (SELECT ST_Transform(ST_Buffer(CDB_LatLng(40.7146153,-74.0145634)::geography, 75)::geometry, 4326) As the_geom) As gs
WHERE
  (ST_Intersects(CDB_LatLng(pickup_latitude, pickup_longitude), gs.the_geom)
 OR
  ST_Intersects(CDB_LatLng(dropoff_latitude, dropoff_longitude), gs.the_geom)) AND
  tpep_pickup_datetime >= ('2015-08-21T06:00:00') AND
  tpep_pickup_datetime <= ('2015-08-21T20:00:00')
ORDER BY hour_of_day ASC
```

### Ingoing versus outgoing at different times of the day

```sql
SELECT
  ST_Transform(
    ST_MakeLine(
      CDB_LatLng(pickup_latitude, pickup_longitude),
      CDB_LatLng(dropoff_latitude, dropoff_longitude)),
    3857) As the_geom_webmercator,
  cartodb_id,
  count(*) OVER (PARTITION BY date_part('hour', tpep_pickup_datetime)),
  date_part('hour', tpep_pickup_datetime) as hour_of_day,
  CASE WHEN ST_Intersects(CDB_LatLng(pickup_latitude, pickup_longitude), gs.the_geom) THEN 'pickup' ELSE 'dropoff' END As ingoing_outgoing
FROM
  taxi_aug_21_22_2015 As t,
  (SELECT the_geom FROM ny_boroughs WHERE boroname = 'Manhattan') As mnhtn,
  (SELECT ST_Transform(ST_Buffer(CDB_LatLng(40.7146153,-74.0145634)::geography, 75)::geometry, 4326) As the_geom) As gs
WHERE
  (ST_Intersects(CDB_LatLng(pickup_latitude, pickup_longitude), gs.the_geom)
 OR
  ST_Intersects(CDB_LatLng(dropoff_latitude, dropoff_longitude), gs.the_geom)) AND
  tpep_pickup_datetime >= ('2015-08-21T07:00:00') AND
  tpep_pickup_datetime <= ('2015-08-21T017:00:00')
  order by hour_of_day asc
```


### Taxi Commute rides to/from Manhattan

Start in the outer boroughs in the morning, return to them in the evening. We need additional information: the shapes of the boroughs. Grab them from here:

```text
http://eschbacher.cartodb.com/api/v2/sql?q=SELECT%20*%20from%20ny_boroughs&format=geojson&filename=ny_boroughs
```

Let's look only at rides which originate in Manhattan and end in one of the other four boroughs.

```sql
SELECT
  ST_Transform(
    ST_MakeLine(
      CDB_LatLng(pickup_latitude, pickup_longitude),
      CDB_LatLng(dropoff_latitude, dropoff_longitude)),
    3857) As the_geom_webmercator,
  cartodb_id
FROM
  taxi_aug_21_22_2015 As t,
  (SELECT the_geom FROM ny_boroughs WHERE boroname = 'Manhattan') As mnhtn,
  (SELECT the_geom FROM ny_boroughs WHERE boroname <> 'Manhattan') As boros
WHERE
  ST_Intersects(CDB_LatLng(pickup_latitude, pickup_longitude), mnhtn.the_geom)
 AND
  ST_Intersects(CDB_LatLng(dropoff_latitude, dropoff_longitude), boros.the_geom)
```

### Going to JFK

```sql
SELECT
  ST_Transform(
    ST_MakeLine(
      CDB_LatLng(pickup_latitude, pickup_longitude),
      CDB_LatLng(dropoff_latitude, dropoff_longitude)),
    3857) As the_geom_webmercator,
  cartodb_id
FROM
  taxi_aug_21_22_2015 As t,
  (SELECT the_geom FROM ny_boroughs WHERE boroname = 'Manhattan') As mnhtn,
  (SELECT ST_Transform(ST_Buffer(CDB_LatLng(40.6413, -73.7781)::geography, 1000)::geometry, 4326) As the_geom) As jfk
WHERE
  ST_Intersects(CDB_LatLng(pickup_latitude, pickup_longitude), mnhtn.the_geom)
 AND
  ST_Intersects(CDB_LatLng(dropoff_latitude, dropoff_longitude), jfk.the_geom)
```

We can ID which terminals--and maybe even which airline!--people are going to at different times of the day!

Newark International is at `(40.6895, -74.1745)`, LaGuardia is at `(40.7769, -73.8740)`

```sql
SELECT
  ST_Transform(
    ST_MakeLine(
      CDB_LatLng(pickup_latitude, pickup_longitude),
      CDB_LatLng(dropoff_latitude, dropoff_longitude)),
    3857) As the_geom_webmercator,
  cartodb_id
FROM
  taxi_aug_21_22_2015 As t,
  (SELECT the_geom FROM ny_boroughs WHERE boroname = 'Manhattan') As mnhtn,
  (SELECT ST_Transform(ST_Buffer(CDB_LatLng(40.6413, -73.7781)::geography, 1000)::geometry, 4326) As the_geom
   UNION
   SELECT ST_Transform(ST_Buffer(CDB_LatLng(40.6895, -74.1745)::geography, 1000)::geometry, 4326)
   UNION
   SELECT ST_Transform(ST_Buffer(CDB_LatLng(40.7769, -73.8740)::geography, 1000)::geometry, 4326)) As airports
WHERE
  ST_Intersects(CDB_LatLng(pickup_latitude, pickup_longitude), mnhtn.the_geom)
 AND
  ST_Intersects(CDB_LatLng(dropoff_latitude, dropoff_longitude), airports.the_geom)
```
