##Link to the gist: http://bit.ly/ccleaflet

##Data file to use

We will create the visualization using GeoJSON which is a format for encoding a variety of geographic data structure. 
It follows the following structure:
```
{
        "type": "Feature",
        "geometry": {
          "type": "Point",
          "coordinates": [125.6, 10.1]
        },
        "properties": {
          "name": "Dinagat Islands"
        }
}
```

SQL API to call our compiled and cleaned data (obtained from Kaggle) : 
```
https://mehak-carto.cartodb.com/api/v2/sql?q=SELECT%20*%20FROM%20primary_results_transposed_simplified&format=geojson&filename=primary_results_transposed_simplified
```

##Displaying the Basemap Tiles

```
var map = L.map('map').setView([39.0119, -98.4842], 5);
			
		L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
			attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="https://carto.com/attributions">CARTO</a>'
		}).addTo(map);

```
You can also create your custom basemaps in Mapbox and access them here or also bring in Stamen tiles instead.

##Adding Colors

We create a symbolic map with a gradient of colors reflecting the fraction of votes for the Democratic Party in the Primary elections 2016 for each county in the country. For this we create a function that defines the colors for each vote_fraction bracket according to our predefined brackets. 

```

	function getColor(b) {
			return b <=1.0 & b>=0.85 ? '#9e0142' :
			       b <0.85 & b>=0.7 ? '#d53e4f' :
				b < 0.7 & b>=0.55 ? '#f46d43':
				b <0.55 & b>=0.4 ? '#fdae61':
				b <0.4 &  b>=0.35 ? '#abdda4':
				b < 0.35 & b>=0.2 ? '#66c2a5':
			       b < 0.2 & b>=0.05 ? '#3288bd' :
			       b < 0.05 & b>=0 ? '#5e4fa2' :
			       			'#878787' ;
		}
```
Since this function takes in the fraction votes parameter, while defining the overall style function for the feature of our GeoJSON data, we access the ```feature.properties.bernie_fraction``` while calling the ```getColor``` function.

```
	function style(feature) {
			return {
				weight: 0.6,
				opacity: 1,
				color: 'white',
				dashArray: '2',
				fillOpacity: 0.6,
				fillColor: getColor(feature.properties.bernie_fraction)
			};
		}
```
##Adding Interaction while Hover

We next create a function ```highlightFeature()``` that takes in the event object and highlights the target layer (i.e. the layer over which the user hovers) with the styling properties mentioned in the options. We use the ```setStyle()```, a pre-defined method in Leaflet. We also make sure, that the highlights of the hovered feature do not clash with the existing layer features by the ```bringToFront()``` method. Since, this method has issues with Internet Explorer and Mobile Opera we want to make sure that we do not apply this on either of those platforms by this condition ```if (!L.Browser.ie && !L.Browser.opera)```. 

```
function highlightFeature(e) {
			var layer = e.target;

			layer.setStyle({
				weight: 3,
				color: 'grey',
				dashArray: '',
				fillOpacity: 0.7
			});

			if (!L.Browser.ie && !L.Browser.opera) {
				layer.bringToFront();
			}

			info.update(layer.feature.properties);
		}
```
To define what happens when the mouse is not hovering over any of the counties, we define the following function:

```
var geojson;

		function resetHighlight(e) {
			geojson.resetStyle(e.target);
			info.update();
		}
```
The ```resetStyle``` method in leaflet helps reset the style of the target feature to the original GeoJSON style, particularly useful in post-hover cases like this.
We also use the info.update() function within our functions defining interaction which is defined as follows:

```
var info = L.control();

		info.onAdd = function(map) {
			this._div = L.DomUtil.create('div', 'info');
			this.update();
			return this._div;
		};
		
		info.update = function(props) {
			this._div.innerHTML = '<h4>US Primary Election Data 2016</h4>' +  '<br />' + (props ?
				props.county + ' County' + '<br />' + '<br />' +
				'<b>Hillary # of votes: ' + props.hillary_votes + '</b><br />' +
				 'Fraction of votes: ' + props.hillary_fraction + '<br />' + '<br />' +
				 '<b>Bernie # of votes: ' + props.bernie_votes + '</b><br />' +
				'Fraction of votes: ' + props.bernie_fraction
				: 'Hover over a county');
		};

		info.addTo(map);
```
This creates a custom control to update the information of each county as the user hovers over it. We also use an ```info.onAdd``` function that adds the information on the map as the layers are loaded. 

```
info.onAdd = function (map) {
			this._div = L.DomUtil.create('div', 'info');
			this.update();
			return this._div;
		};
```
The ```L.DomUtil.create()``` creates a DOM node (div element here) and assigns it to the class 'info'. This element is added at the time of map loading on the map using ```info.addTo(map);```

To add a little more custom interactivity, we also define a function ```zoomToFeature``` that zooms into the bounds of the county which is clicked on by the user.

```
	function zoomToFeature(e) {
			map.fitBounds(e.target.getBounds());
		}
```
This is achieved by the ```fitBounds()``` method of altering the map state by assigning the bounds recieved by using the ```getBounds()``` method on the target layer.

##Putting it all together!

Next, we use the ```onEachFeature``` option that will be called on each created feature layer to define what happens on  ```mouseover```, ```mouseout``` and ```click``` events. And finally, adding the GeoJSON with the defined ```style``` and ```onEachFeature``` option, we add the layer and its interactivity to the map using ```addTo(Map)```.

```
function onEachFeature(feature, layer) {
			console.log('onEachFeature was entered');
			layer.on({
				mouseover: highlightFeature,
				mouseout: resetHighlight,
				click: zoomToFeature
			});
		}

		$.getJSON ("https://mehak-carto.cartodb.com/api/v2/sql?q=SELECT%20*%20FROM%20primary_results_transposed_simplified%20&format=geojson&filename=primary_results_transposed_simplified", function(data) {
			console.log('geojson retrieved');
			geojson = L.geoJson(data, {
				style: style,
				onEachFeature: onEachFeature
			}).addTo(map);
		});
```

##Adding Legend to the Map

Next we construct and add the legend to the map. 

```
	var legend = L.control({position: 'bottomright'});

		legend.onAdd = function (map) {

			var div = L.DomUtil.create('div', 'info legend'),
				grades = [1.0, 0.85, 0.7, 0.55, 0.40, 0.35, 0.2, 0.05],
				labels = ['<strong>Fraction Vote Bernie Sanders</strong>'],
				from, to;
			var x=0.99;

			for (var i = 0; i < grades.length; i++) {
				from = grades[i];
				to = grades[i + 1];

				labels.push(
					'<i style="background:' + getColor(x,1-x) + '"></i> ' +
					from + (to ? '&ndash;' + to : '+'));
					x-=0.14;
			}

			div.innerHTML = labels.join('<br>');
			return div;
		};

		legend.addTo(map);
```
In this function, the ```DomUtil``` option creates a ```div``` element within the ```info legend``` class and assigns the range to the grade array. Using the loop, we assign the grade brackets to the colors by the ```getColor``` function. Finally, the ```labels.join()``` option adds format to the legend labels and it is finally added to the map with ```addTo(map)```.
