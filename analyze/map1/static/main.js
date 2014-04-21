
// uses backbone, underscore, d3, topojson

var PublicModule = (function() {
    "use strict";
    var startDate;
    var endDate;

    var allTweets;
    var tweetsToShow;
    var width=1024, height=768;

    var svg = d3.select("#mainSvg")
        .attr("width", width)
        .attr("height", height);

    var projection = d3.geo.mercator()
        .center([-79.98, 40.431667]) //-80, 40.441667 is the center of pgh
        .scale(230000) // ad hoc hacky, works
        .translate([width/2, height/2]);

    // points for the query box, in [lon, lat] form
    var bboxTopLeft = [];
    var bboxBottomRight = [];

    // Two synced arrays; neighborhoods is the data, Names is just the names.
    var neighborhoods = [];
    var neighborhoodNames = [];

    // transforms a ... GeometryCollection?... object into a svg path 'd' string
    var path = d3.geo.path().projection(projection);
    // transforms a tweet object into a svg path 'd' string
    var tweetsPath = function(tweet) {
        // some tweets don't have coordinates, just a tweet.place.bounding_box
        // (which can be huge, like 7 degrees lat or lon, so forget it)
        // Note that there is still useful info in tweet.place (like "Pittsburgh")
        // Anyway I think path(null) just returns null, which works ok
        return path(tweet.coordinates);
    }
    var params;

    // Given an array of tweets, return the ones that are between the values in
    // startDate and endDate
    var filterDates = function(tweets, startDate, endDate) {
        var tweetsToShow = tweets;
        if (startDate != null) {
            tweetsToShow = tweetsToShow.filter(function(e) {return new Date(e.created_at) >= startDate;});
        }
        if (endDate != null) {
            tweetsToShow = tweetsToShow.filter(function(e) {return new Date(e.created_at) <= endDate;});
        }
        return tweetsToShow;
    };

    // Returns a color, given a tweet. All tweets from the same user should have
    // the same color.
    var generateTweetColor = function(tweet) {
        var id = tweet.user.id;
        var hex = (id & 0xffffff).toString(16);
        return '#' + hex;
    };

    var update = function() {
       
        var tweetSelection = svg.selectAll(".tweet")
            .data(tweetsToShow)
            .style("fill", generateTweetColor)
            .attr("d", tweetsPath);

        tweetSelection.enter().append("path") // .enter() means "if there's more data than dom elements, do this for each new one"
            .attr("d", tweetsPath)
            .attr("class", "tweet")
            .style("fill", generateTweetColor)
            .on("click", function(tweet) {
                console.log(tweet.id + "\t " + tweet.user.screen_name + ": " + tweet.text);
            });
        tweetSelection.exit().remove();
        $("#status").text("Tweets: " + allTweets.length + ", Displaying: " + tweetsToShow.length);

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
            // pointInPolygons because each Neighborhood can be made up of many polygons.
            if (pointInPolygons(point, neighborhoods.features[i].geometry.coordinates)) {
                return neighborhoodNames[i];
            }
        }
        return "Outside Pittsburgh";
    };


    var Module = {
        // TODO remove, this is for debugging
        getNghds: function() {
            return neighborhoods;
        },

        loadNeighborhoods: function() {
            d3.json("static/neighborhoodstopo.json", function(error, nghds) {
                neighborhoods = topojson.feature(nghds, nghds.objects.neighborhoods);
                svg.append("path")
                    .datum(neighborhoods)
                    .attr("d", path)
                    .attr("class", "neighborhood");
            });
            // load the geojson file, just for the names.
            d3.json("static/neighborhoods.json", function(error, nghds) {
                console.log(nghds);
                for(var i = 0; i < nghds.features.length; i++) {
                    neighborhoodNames[i] = nghds.features[i].properties.HOOD;
                }
            });
        },

        storePoint: function(x, y) {
            var geoPoint = projection.invert([x, y]);
            bboxTopLeft = geoPoint;
                
            $("#topLeftCoords").text(bboxTopLeft[0].toFixed(4) + ", " + bboxTopLeft[1].toFixed(4));
            $("#status").text(neighborhoodName(geoPoint));
        },

        selectTweetsToShow: function() {
            var startDate = $("#startDate").datepicker("getDate");
            var endDate = $("#endDate").datepicker("getDate");
            var startHour = $("#startTime").val();
            var endHour = $("#endTime").val();

            var goodTweets = _.filter(allTweets, function(tweet) {
                var tweetDate = new Date(tweet['created_at']);
                if (startDate != null && tweetDate < startDate) {
                    return false;
                }
                if (endDate != null && tweetDate > endDate) {
                    return false;
                }
                var tweetHour = tweetDate.getHours();
                if (tweetHour >= endHour || tweetHour < startHour) {
                    return false;
                }
                return true;
            });
            tweetsToShow = _.sample(goodTweets, $("#display_limit").val());
            update();
        },

        // returns tweets by people who most commonly tweet in the
        // neighborhood you've clicked on.
        tweetsByThisNghdUsersQuery: function() {
            params = {"limit": $("#server_limit").val(),
                    "lon": bboxTopLeft[0], "lat": bboxTopLeft[1]};
            $.getJSON("/tweets_by_this_nghd_users", params, function(tweets) {
                allTweets = tweets.results;
                tweetsToShow = _.sample(allTweets, $("#display_limit").val());
                update();
            });

            $("#loading").show();
        },

        // Just get a bunch of tweets from the server. (You won't show them all at
        // the same time.)
        getBunchOfTweets: function() {
            params = {
                "limit": $("#server_limit").val()
            }
            $.getJSON("/bunch_of_tweets", params, function(tweets) {
                allTweets = tweets.results;
                tweetsToShow = _.sample(allTweets, $("#display_limit").val());
                update();
            });

            $("#loading").show();
        },

        update: update, // make this publicly accessible
    };
    return Module;
}());

