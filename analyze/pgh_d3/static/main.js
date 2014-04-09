
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
            .attr("d", path)
            .attr("class", "neighborhood");
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
    $("#loading").show();
}

// Returns a color, given a tweet. All tweets from the same user should have
// the same color.
function generateTweetColor(tweet) {
    var id = tweet.user.id;
    var hex = (id & 0xffffff).toString(16);
    return '#' + hex;
}

function update() {
   
    var tweetSelection = svg.selectAll(".tweet")
        .data(tweetsToShow)
        .style("fill", generateTweetColor)
        .attr("d", tweetsPath);
    // The result of data() is the "update" selector, so anything you put here
    // will update when the backing data array (tweetsToShow here) changes.

    tweetSelection.enter().append("path") // .enter() means "if there's more data than dom elements, do this for each new one"
        .attr("d", tweetsPath)
        .attr("class", "tweet")
        .style("fill", generateTweetColor)
        .on("click", function(tweet) {
            console.log(tweet.id + "\t " + tweet.user.screen_name + ": " + tweet.text);
        });
    tweetSelection.exit().remove();

    $("#loading").hide()
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

// returns the string name of the collection to query from
function getCollection() {
    if ($("#useTweets").prop("checked")) {
        return "tweet_pgh_good";
    } else if ($("#useFoursquare").prop("checked")) {
        return "foursquare";
    } else {
        alert("error: no collection selected");
    }
}

// Gets all tweets from all users whose tweet-centroids are within the box
// you've drawn.
function userCentroidQuery() {
    params = {"top_left_lon": bboxTopLeft[0], "top_left_lat":bboxTopLeft[1],
        "bottom_right_lon": bboxBottomRight[0], "bottom_right_lat": bboxBottomRight[1],
        "start_hour": $("#startTime").val(),
        "end_hour": $("#endTime").val(),
        "limit": $("#limit").val(),
        "per_user_limit": $("#per_user_limit").val(),
        "collection": getCollection()};
    $.getJSON("/user_centroid_query", params, function(tweets) {
        allTweets = tweets.results;
        tweetsToShow = filterDates(allTweets,
            $("#startDate").datepicker("getDate"),
            $("#endDate").datepicker("getDate"));
        update();
    });
    $("#loading").show();

}

// Gets all tweets from any users who have ever tweeted in the box you've drawn.
function userHereOnceQuery() {
    params = {"top_left_lon": bboxTopLeft[0], "top_left_lat":bboxTopLeft[1],
        "bottom_right_lon": bboxBottomRight[0], "bottom_right_lat": bboxBottomRight[1],
        "start_hour": $("#startTime").val(),
        "end_hour": $("#endTime").val(),
        "limit": $("#limit").val(),
        "per_user_limit": $("#per_user_limit").val(),
        "collection": getCollection()};
    $.getJSON("/user_here_once_query", params, function(tweets) {
        allTweets = tweets.results;
        tweetsToShow = filterDates(allTweets,
            $("#startDate").datepicker("getDate"),
            $("#endDate").datepicker("getDate"));
        update();
    });

    $("#loading").show();
}

// Just get a bunch of tweets from the server. (You won't show them all at
// the same time.)
function getBunchOfTweets() {
    params = {
        "limit": $("#limit").val()
    }
    $.getJSON("/bunch_of_tweets", params, function(tweets) {
        allTweets = tweets.results;
        tweetsToShow = allTweets.slice(0,1000);
        update();
    });

    $("#loading").show();
}
