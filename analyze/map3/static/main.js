
// uses backbone, underscore, d3, topojson

var allTweets = [];
var tweetsToShow = [];
var width=1024, height=768;

var svg = d3.select("#mainSvg")
    .attr("width", width)
    .attr("height", height);

var projection = d3.geo.mercator()
    .center([-79.98, 40.431667]) //-80, 40.441667 is the center of pgh
    .scale(230000) // ad hoc hacky, works
    .translate([width/2, height/2]);

// points for the query box, in [lon, lat] form
var storedPoint = [];

// Two synced arrays; neighborhoods is the data, Names is just the names.
var neighborhoods; // will be a {Type: "FeatureCollection", features: Array[91]}
// and each one is a {type: "Feature", properties: {...}, geometry: {...}}
var neighborhoodNames = [];
var selectedNeighborhood = ''; // name; e.g. "Shadyside"

// the users to be displayed
var users = [];

// transforms a ... GeometryCollection?... object into a svg path 'd' string
var path = d3.geo.path().projection(projection);
// transforms a tweet object into a svg path 'd' string
// var tweetsPath = function(tweet) {
    // some tweets don't have coordinates, just a tweet.place.bounding_box
    // (which can be huge, like 7 degrees lat or lon, so forget it)
    // Note that there is still useful info in tweet.place (like "Pittsburgh")
    // Anyway I think path(null) just returns null, which works ok
//     return path(tweet.coordinates);
// }

// Returns a color, given a tweet. All tweets from the same user should have
// the same color.
var generateTweetColor = function(tweet) {
    var id = tweet.user.id;
    var hex = (id & 0xffffff).toString(16);
    return '#' + hex;
};

var usersPath = function(user) {
    // oops, got to convert the user's centroid to GeoJSON first
    var pt = {"type":"Feature","geometry":{"type":"Point", "coordinates":user.centroid}}
    return path(pt);
};

var getCx = function(user) {
    return projection(user.centroid)[0];
}
var getCy = function(user) {
    return projection(user.centroid)[1];
}
var getR = function(user) {
    return (user['50%radius']+.001) * 10000;
    // TODO ugh why did I save everything in the database as "degrees"?
    // that is not a good measurement for linear distance.
    // this conversion here doesn't actually convert to real distance.
}

var update = function() {
  
    // display the neighborhoods
    var nghdSelection = svg.selectAll(".neighborhood")
        .data(neighborhoods.features)
        .attr("d", path);
    nghdSelection.enter().append("path")
        .attr("class", "neighborhood")
        .attr("d", path);
    nghdSelection.exit().remove();

    // display the users
    var usersSelection = svg.selectAll(".user")
        .data(users)
        .attr("cx", getCx)
        .attr("cy", getCy)
        .attr("r", getR);
        // .attr("d", usersPath);
    usersSelection.enter().append("circle")
        .attr("cx", getCx)
        .attr("cy", getCy)
        .attr("r", getR)
        // .attr("d", usersPath)
        .attr("class", "user");
        
    usersSelection.exit().remove();

    $("#loading").hide();
};

// from https://github.com/substack/point-in-polygon
// point is a pair of x, y; vs is the vertices of the polygon
var pointInPolygon = function (point, vs) {
    //TODO: This function as written was not made to work on MultiPolygons
    // (which a few Pittsburgh neighborhoods are) so here's a hacky fix.
    if (vs.length === 1 && vs[0].length > 1) {
        return pointInPolygon(point, vs[0]);
    }

    // ray-casting algorithm based on
    // http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html
    var x = point[0], y = point[1];
    var inside = false;
    for (var i = 0, j = vs.length - 1; i < vs.length; j = i++) {
        var xi = vs[i][0], yi = vs[i][1];
        var xj = vs[j][0], yj = vs[j][1];
        
        var intersect = ((yi > y) != (yj > y))
            && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
        if (intersect) inside = !inside;
    }
    return inside; 
};
// polygons is an array of arrays of vertices. (one array of vertices = one polygon)
// ugh, I mean, sometimes they are just [[v1,v2...]], sometimes:
// [[ [[v1,v2,...]], [[v10,v11,...]] ]] - I don't know why always double
// arrays. Anyway, there's a hacky fix up in pointInPolygon above too.
var pointInPolygons = function (point, polygons) {
    for (var i = 0; i < polygons.length; i++) {
        if (pointInPolygon(point, polygons[i])) {
            return true;
        }
    }
    return false;
};

// returns the name of the neighborhood that contains this point.
var neighborhoodName = function(point) {
    for (var i = 0; i < neighborhoods.features.length; i++) {
        if (pointInPolygons(point, neighborhoods.features[i].geometry.coordinates)) {
            return neighborhoodNames[i];
        }
    }
    return "Outside Pittsburgh";
};

var loadNeighborhoods = function() {
    d3.json("static/neighborhoodstopo.json", function(error, nghds) {
        neighborhoods = topojson.feature(nghds, nghds.objects.neighborhoods);
        update();
   });
    // load the geojson file, just for the names.
    d3.json("static/neighborhoods.json", function(error, nghds) {
        console.log(nghds);
        for(var i = 0; i < nghds.features.length; i++) {
            neighborhoodNames[i] = nghds.features[i].properties.HOOD;
        }
    });
};

var storePoint = function(x, y) {
    var geoPoint = projection.invert([x, y]);
    storedPoint = geoPoint;

    $("#topLeftCoords").text(storedPoint[0].toFixed(4) + ", " + storedPoint[1].toFixed(4));
    selectedNeighborhood = neighborhoodName(geoPoint);
    $("#status").text(selectedNeighborhood);
};

var getUsersInNeighborhood = function() {
    var params = {"nghd": neighborhoodName(storedPoint)};
    $.getJSON("/nghd_users", params, function(results) {
        console.log(results);
        users = results['results'];
        update();
    });
    
};

