
var startDate;
var endDate;

var allTweets;
var tweetsToShow;

var width = 1024,
    height = 768;

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

function loadNeighborhoods() {
    d3.json("static/neighborhoodstopo.json", function(error, nghds) {
        var neighborhoods = topojson.feature(nghds, nghds.objects.neighborhoods);
        svg.append("path")
            .datum(neighborhoods)
            .attr("d", path);
    });
}

// Given an array of tweets, return the ones that are between the values in
// startDate and endDate
function filterDates(tweets, startDate, endDate) {
    var tweetsToShow = tweets;
    if (startDate != null) {
        tweetsToShow = tweetsToShow.filter(function(e) {return new Date(e.created_at) >= startDate;});
    }
    if (endDate != null) {
        tweetsToShow = tweetsToShow.filter(function(e) {return new Date(e.created_at) <= endDate;});
    }
    return tweetsToShow;
}

function runQuery() {
    params = $.parseJSON( $("#query").val() ); // TODO sanitize, obv
    // takes about a second per 1k tweets. crashes on 100k.
    $.getJSON("/query", JSON.stringify(params), function(tweets) {
        allTweets = tweets.results;
        update();
    });
 }

function update() {
    tweetsToShow = filterDates(allTweets,
        $("#startDate").datepicker("getDate"),
        $("#endDate").datepicker("getDate"));
   
    var tweetSelection = svg.selectAll(".tweet").data(tweetsToShow);
    tweetSelection.enter().append("path") // .enter() means "if there's more data than dom elements, do this for each new one"
        .attr("class", "tweet")
        .on("click", function(tweet) {
            console.log(tweet.user.screen_name + ": " + tweet.text);
        });
    tweetSelection.attr("d", tweetsPath); //TODO is this not right?
    tweetSelection.exit().remove();

}

function storeBoundingBoxPoint(x, y) {
    var geoPoint = projection.invert([x, y]);
    if (bboxTopLeft.length == 0) {
        bboxTopLeft = geoPoint;
    } else if (bboxBottomRight.length == 0) {
        bboxBottomRight = geoPoint;
    } else { // top left and bottom right both already exist, start new ones
        bboxTopLeft = geoPoint;
        bboxBottomRight = [];
    }
    $("#topLeftCoords").text(bboxTopLeft);
    $("#bottomRightCoords").text(bboxBottomRight);
}

// Gets all tweets from all users whose tweet-centroids are within the box
// you've drawn.
function userCentroidQuery() {
    params = {"top_left_lon": bboxTopLeft[0], "top_left_lat":bboxTopLeft[1],
        "bottom_right_lon": bboxBottomRight[0], "bottom_right_lat": bboxBottomRight[1],
        "limit": $("#limit").val()};
    $.getJSON("/user_centroid_query", params, function(tweets) {
        allTweets = tweets.results;
        update();
    });

}

// Gets all tweets from any users who have ever tweeted in the box you've drawn.
function userHereOnceQuery() {
    params = {"top_left_lon": bboxTopLeft[0], "top_left_lat":bboxTopLeft[1],
        "bottom_right_lon": bboxBottomRight[0], "bottom_right_lat": bboxBottomRight[1],
        "limit": $("#limit").val()};
    $.getJSON("/user_here_once_query", params, function(tweets) {
        allTweets = tweets.results;
        update();
    });

}
