# OpenStreetMap Overpass API

![alt text](http://wiki.openstreetmap.org/w/images/7/79/Public-images-osm_logo.svg "OpenStreetMap") ![alt text](http://wiki.openstreetmap.org/w/images/thumb/b/b5/Overpass_API_logo.svg/800px-Overpass_API_logo.svg.png "Overpass API")

OpenStreetMap's [Overpass API](http://wiki.openstreetmap.org/wiki/Overpass_API) is a "read-only API that serves up custom selected parts of the OSM map data." This CartoCamp workshop is an introduction to the query language of Overpass and how you can use it to obtain points, lines, and shapes for your maps.

## Requirements
There are no installation requirements for this workshop, but if you would like to incorporate API results into a map right away, you should get a free CARTO account. Signup for an account here: <https://carto.com/signup>

## Overpass Turbo
[Overpass Turbo](http://overpass-turbo.eu/) is a "web-based data filtering tool" with a built-in wizard that makes constructing simple queries less of a headache. It also allows you to preview the data before downloading or exporting. If you want to start making more advanced queries, it's recommended to use Overpass Turbo to help you experiment and get familiar with the query language structure.

### Let's Unpack a Simple Overpass Turbo Query

In the Overpass Turbo Wizard, type the following query and select build:

```
tourism=museum in "New York"
```

Let's take a look at the query that Overpass Turbo just built:

![alt text](https://cl.ly/112e1f063A2l/Image%202017-03-02%20at%205.25.35%20PM.png "overpass turbo wizard build")

Parts of this query:

1. Settings for the output format and timeout
2. An area for the search is defined with [`geocodeArea`](http://wiki.openstreetmap.org/wiki/Overpass_turbo/Extended_Overpass_Turbo_Queries)
3. The query for a key-value pair `tourism=museum` tag on a [union](http://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#Union) of [`nodes`](http://wiki.openstreetmap.org/wiki/Node), [`ways`](http://wiki.openstreetmap.org/wiki/Way), and [`relations`](http://wiki.openstreetmap.org/wiki/Relation).
4. There is a _recursion_ down [`>;`](http://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#Recurse_down_.28.3E.29)
5. Results are printed out twice, as `body` and `skel qt`

Some other things to note about the query:

- The query is a string of statements, each statement ending with a semicolon. The statements are processed one after another.
- Statements can be:
	- Standalone queries: These are complete statements on their own.
	- Filters: They are always part of a query statement and contain the interesting selectors and filters.
	- Block statements: They group statements and enable disjunctions as well as loops.
	- Settings: Things like output format and timeout that can be set once at the beginning.

[Run the query](http://overpass-turbo.eu/s/nbx) and check out what is returned in map-view and data-view.

![alt text](https://d3uepj124s5rcx.cloudfront.net/items/3w2I0s2V013b0U332B43/Image%202017-03-02%20at%205.00.30%20PM.png?v=39753a48 "map view of museums in ny")

## Export the data to a map

Select Export -> Data -> and download the geojson file.

![alt text](https://d3uepj124s5rcx.cloudfront.net/items/0q1Y433734333y351s14/Image%202017-03-02%20at%205.03.10%20PM.png?v=4d32d468 "geojson export")

Go to your CARTO account or your favorite map editing tool, make a new dataset or map. Upload the geojson file.

After the import has finished, view your new map!

![alt text](https://cl.ly/1F070s272i1Q/Image%202017-03-02%20at%205.08.13%20PM.png "museums in CARTO")

## Museums in multiple cities

Let's make use of block statements to create a **union** of search areas. In this query, we're looking for museum locations in both Boston and New York. We simply add in another geocodeArea for Boston inside parenthesis. Nothing else has changed about the query.

```
[out:json][timeout:25];
({{geocodeArea:New York}};{{geocodeArea:Boston}})->.searchArea;
(
  node["tourism"="museum"](area.searchArea);
  way["tourism"="museum"](area.searchArea);
  relation["tourism"="museum"](area.searchArea);
);
out body;
>;
out skel qt;
```

## Why Overpass is awesome!

- Quick, easy single resource for most of the world's shapes
- Try searching Google for "museum locations Boston and New York shapefile" ... this data doesn't exist ready for consumption.
- [Official NYC Museums Locations](
https://data.cityofnewyork.us/Recreation/New-York-City-Museums/ekax-ky3z) from NYC Open Data
- Boston doesn't appear to have a museum shapefile readily available at the moment
- You would still need to join the layers together and do custom filtering to get the same results.

## Why this might not be as awesome...

- OSM is like the Wikipedia of human location knowledge. Anyone can add or edit the data. The source needs to be double-checked. Information might be outdated, wrong, or missing!
- Overpass query language can be difficult to work with. But Overpass Turbo can help in the learning and experimental process.
- Overpass doesn't do so great with bulk downloads of lots of data points.

## Search for playgrounds around schools
You can also chain queries to get output satisfying a second criterion that are located around nodes matching the first criterion. In this example, we find parks within 100m of schools in NYC:

```
/*
Find parks within 100m of schools in NYC
*/
[out:json];
{{geocodeArea:New York}}->.searchArea;
  node[amenity='school'](area.searchArea);
(node
  (around:100)
  [leisure="park"];
way
  (around:100)
  [leisure="park"]);
out body;
>;
out skel qt;
```

## More Reources

- Tons of [examples](http://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_API_by_Example)
- What kind of tags can I filter by? Track all OSM tags [here](<https://taginfo.openstreetmap.org>).
- [CartoCamp LearnOverpass](http://michellemho.github.io/learnoverpass//en/)