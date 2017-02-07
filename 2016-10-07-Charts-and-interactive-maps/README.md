##Link to the gist: http://bit.ly/CartoCampII

Inspiration: 
http://www.nytimes.com/elections/2016/national-results-map

http://chriswhong.github.io/nycSchools/

##Data file to use

Collection and wrangling of data:
http://bit.ly/dataelection

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

SQL API to call our compiled and cleaned data (obtained from json) : 
"https://mehak-carto.cartodb.com/api/v2/sql?q=SELECT%20*%20FROM%20finalest%20&format=geojson&filename=finalest"


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
			return b <= 0.0 & b> -0.25 ? '#85c4c9' :
                   b <= -0.25 & b > -0.5 ? '#4f90a6':
                   b <= -0.5 & b> -0.75 ? '#3b738f':
                   b <= -0.75 & b>= -1.0 ? '#2a5674':
			       b > 0.0 & b <= 0.25 ? '#facba6' :
                   b > 0.25 & b <= 0.5 ? '#f8b58b':
                   b > 0.5 & b <= 0.75 ? '#f2855d':
                   b > 0.75 & b <= 1.0 ? '#eb4a40':
			    			'grey' ;
		}
```
Since this function takes in the fraction votes parameter, while defining the overall style function for the feature of our GeoJSON data, we access the ```feature.properties.bernie_fraction``` while calling the ```getColor``` function.

```
	function style(feature) {
			return {
				weight: 0.6,
				opacity: 0.4,
				color: 'white',
				fillOpacity: 0.8,
				fillColor: getColor(feature.properties.frac_tot)
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
            if (props) {
                if (props.party == 'Democratic') {
                    var labels = ['Hillary Clinton', 'Bernie Sanders'];
                    var data = [props.clinton_1746_president, props.sanders_1445_president];
                    console.log('labels', labels, 'data', data);
                    var dems = '<h4>US Primary Election Data 2016</h4>' +  '<br />' + (props ? props.name + ' County' + '<br />' + '<br />' + '<b>Democratic Party Winner: ' + props.d_winner + '</b><br />'+ 'Margin of Victory (%): ' + props.d_margin_pc.toFixed(2):'mehak');
                    dems += '<canvas id="myChart" width="10" height="10"></canvas>';
                    this._div.innerHTML = dems;
                    newChart(labels, data);
                } else {
                    var labels = ['Trump', 'Cruz','Kasich','Rubio'];
                    var data = [props.trump_8639_president, props.cruz_61815_president, props.kasich_36679_president, props.rubio_53044_president];
                    var reps = '<h4>US Primary Election Data 2016</h4>' +  '<br />' + (props ? props.name + ' County' + '<br />' + '<br />' + '<b>Republican Party Winner: ' + props.r_winner + '</b><br />'+ 'Margin of Victory (%): ' + props.r_margin_pc.toFixed(2):'andy');
                    reps += '<canvas id="myChart" width="10" height="10"></canvas>';
                    this._div.innerHTML = reps;
                    newChart(labels, data);
                }
            }

                console.log('props:', props);
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

The L.DomUtil.create() creates a DOM node (div element here) and assigns it to the class 'info'. This element is added at the time of map loading on the map using info.addTo(map);


##Charts

http://www.chartjs.org/docs/

```
var newChart = function(labels, data) {
        var dataLength = labels ? labels.length : 0;
        console.log
        console.log('we\'re in newChart', labels, data);
        var backgroundColors = ['rgba(235,127,134, 0.9)',
                                'rgba(206,102,147, 0.9)',
                                'rgba(129,55,83, 0.9)',
                                'rgba(211,156,131, 0.9)',
                                'rgba(153, 102, 255, 0.9)',
                                'rgba(255, 159, 64, 0.9)'];
        var colors = [];
        for (var i = 0; i < dataLength; i++) {
            colors.push(backgroundColors[i]);
        };
        console.log('newChart colors', colors);
        var ctx = document.getElementById("myChart");
        var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: '# of Votes',
                        data: data,
                        backgroundColor: colors,
                        borderColor: colors,
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero:true
                            }
                        }]
                    }
                }
            });
    };
```

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
				grades = [100, 75, 50, 25, 0, 25, 50, 75, 100],
				labels = ['<strong>Party Bent</strong>'],
				from, to;
			var x=1;
            var y=1;
			for (var i = 0; i < grades.length - 1; i++) {
				from = grades[i];
				to = grades[i + 1];
                y++;

				labels.push(
					'<i style="background:' + getColor(x,x-0.25) + '"></i> ' + from + (' to ' + to)
                    );
					x-=0.25;
			}

			div.innerHTML = labels.join('<br>');
			return div;
		};

		legend.addTo(map);
		
```
In this function, the ```DomUtil``` option creates a ```div``` element within the ```info legend``` class and assigns the range to the grade array. Using the loop, we assign the grade brackets to the colors by the ```getColor``` function. Finally, the ```labels.join()``` option adds format to the legend labels and it is finally added to the map with ```addTo(map)```.
