
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


    var Module = {

        loadNeighborhoods: function() {
            d3.json("static/neighborhoodstopo.json", function(error, nghds) {
                var neighborhoods = topojson.feature(nghds, nghds.objects.neighborhoods);
                svg.append("path")
                    .datum(neighborhoods)
                    .attr("d", path)
                    .attr("class", "neighborhood");
            });
        },

        storePoint: function(x, y) {
            var geoPoint = projection.invert([x, y]);
            bboxTopLeft = geoPoint;
                
            $("#topLeftCoords").text(bboxTopLeft[0].toFixed(4) + ", " + bboxTopLeft[1].toFixed(4));
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

