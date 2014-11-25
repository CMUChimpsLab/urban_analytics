// Here's where we're calling the google maps API. No API key needed yet, b/c
// we're not using it very much. If we started using it enough that we wanted
// to track our usage, we should get an API key. More info:
// https://developers.google.com/maps/documentation/javascript/tutorial#api_key
//
// And that "async!" is from the async plugin.
// https://github.com/millermedeiros/requirejs-plugins
define(['async!//maps.googleapis.com/maps/api/js?language=en&libraries=drawing,places,visualization'], function () {
    return function (canvas, dataPanel) {
        var latitude = 40.4417, // default pittsburgh downtown center
            longitude = -80.0000;
        var marks = {};
        // var markers = [];
        // var circles = [];
        var redDotImg = 'static/images/maps_measle_red.png';
        var blueDotImg = 'static/images/maps_measle_blue.png';
        var mapOptions = {
            center: {lat: latitude, lng: longitude},
            zoom: 14,
        };
        var map = new google.maps.Map(canvas, mapOptions);

        // add user search UI
        var input = document.createElement('input');
        input.setAttribute("id", "user-screen-name-input");
        input.setAttribute("placeholder", "Twitter Screen Name");
        var userSearchDiv = document.createElement('div');
        userSearchDiv.setAttribute("id", "userSearchDiv");
        // var btn = document.createElement('button');
        // btn.setAttribute("id", "get-user-tweet-range-btn");
        // btn.innerText = "Create Map";
        userSearchDiv.appendChild(input);
        // userSearchDiv.appendChild(btn);
        userSearchDiv.index = 1;
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(userSearchDiv);

        // add function UI
        var functionsDiv = document.createElement('div');
        functionsDiv.setAttribute("id", "functionsDiv");
        var most_tweets_link = document.createElement('a');
        most_tweets_link.setAttribute("id", "most_tweets_link");
        most_tweets_link.innerText = "Get 10 Users Who Tweet The Most";
        most_tweets_link.index = 1;
        functionsDiv.appendChild(most_tweets_link);
        map.controls[google.maps.ControlPosition.BOTTOM_LEFT].push(functionsDiv);

        // bind events
        google.maps.event.addDomListener(most_tweets_link, 'click', function() {
            $.ajax({
                type: "get",
                url: $SCRIPT_ROOT + "/get-top-10-user-tweet-range",
                success: function (response) {
                    api.addRanges(response["tweet_ranges"]);
                },
                error: function () {
                    console.log("ajax request failed for " + this.url);
                }
            });
        });
        google.maps.event.addDomListener(input, 'keyup', function() {
            if(event.keyCode == 13){
                // $("#get-user-tweet-range-btn").click();
                $.ajax({
                    type: "get",
                    data: {user_screen_name: $("#user-screen-name-input").val()},
                    url: $SCRIPT_ROOT + "/get-user-tweet-range",
                    success: function (response) {
                        // api.clearMap();
                        api.addRange(response["tweet_range"]);
                    },
                    error: function () {
                        console.log("ajax request failed for " + this.url);
                    }
                });
            }
        });

        // get the default bounds for a google.maps.Rectangle
        function getDefaultBounds(latitude, longitude) {
            return new google.maps.LatLngBounds(
                new google.maps.LatLng(latitude - 0.002, longitude - 0.004),
                new google.maps.LatLng(latitude + 0.002, longitude + 0.004)
            );
        }

        function prettyPrint(num) {
            return num.toFixed(4);
        }

        function attachTextToMarker(marker, message) {
            var textWindow = new google.maps.InfoWindow({
                content: message
            });

            google.maps.event.addListener(marker, 'click', function() {
                textWindow.open(marker.get('map'), marker);
            });
        }

        function removeMark(key) {
            if (key in marks) {
                var mark = marks[key];
                var markers = mark['markers'];
                if (markers.length > 0) {
                    for(var i = 0; i < markers.length; i++) {
                        markers[i].setMap(null);
                    }
                }

                var circles = mark['circles'];
                if(circles.length > 0) {
                    for(var j = 0; j < circles.length; j++) {
                        circles[j].setMap(null);
                    }
                }
                delete marks[key];
                console.log("removed " + key);
                console.log(marks);
            }
        }

        function plotRange(tweet_range, zoom) {
            console.log("plotting range!");
            console.log(tweet_range);

            if(tweet_range !== null &&
              tweet_range["50%radius"] !== null &&
              tweet_range["90%radius"] !== null &&
              tweet_range["centroid"] !== null &&
              tweet_range["screen_name"] !== null &&
              tweet_range["most_common_neighborhood"] !== null) {
                if (tweet_range["screen_name"] in marks) {
                    return null;
                }
                var username = tweet_range["screen_name"];
                var ngh = tweet_range["most_common_neighborhood"];
                var radius_50 = tweet_range["50%radius"];
                var radius_90 = tweet_range["90%radius"];
                var centroid = tweet_range["centroid"];
                var center = {lat: centroid[1], lng: centroid[0]};

                //Put marker at centroid
                var marker = new google.maps.Marker({
                    position: center,
                    map: map,
                });
                var userText = "<b>" + username + "</b>: " + ngh +
                                "<br /> (" + prettyPrint(centroid[1]) + ", " +
                                prettyPrint(centroid[0]) + ")" +
                                "<br /> 50%: " + radius_50 + ", 90%: " + radius_90;
                attachTextToMarker(marker, userText);
                //Construct the 50% circle
                var Circle50 = new google.maps.Circle({
                    strokeColor: '#FF0000',
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    fillColor: '#FF0000',
                    fillOpacity: 0.35,
                    map: map,
                    center: center,
                    radius: radius_50 //in meters
                });
                //Construct the 90% circle
                var Circle90 = new google.maps.Circle({
                    strokeColor: '#99FFFF',
                    strokeOpacity: 0.9,
                    strokeWeight: 2,
                    fillColor: '#99FFFF',
                    fillOpacity: 0.2,
                    map: map,
                    center: center,
                    radius: radius_90 //in meters
                });

                marks[username] = {'markers': [marker], 'circles': [Circle50, Circle90]};

                if (zoom) {
                    //zoom bounds
                    var southwest = new google.maps.LatLng(centroid[1]-radius_90/50000, centroid[0]-radius_90/50000);
                    var northeast = new google.maps.LatLng(centroid[1]+radius_90/50000, centroid[0]+radius_90/50000);
                    var bounds = new google.maps.LatLngBounds();

                    map.setCenter(center);
                    bounds.extend(southwest);
                    bounds.extend(northeast);
                    map.fitBounds(bounds);
                }
                return username;
            }
            return null;
        }


        function removeRange (username) {
            if (username !== null) {
                removeMark(username);
                $("#" + username + ".user-label").remove();
            }
        }

        function addUserLabel(username) {
            console.log("ADD USER LABEL " + username);
            if (username !== null) {
                icon_src = document.getElementById("remove-icon").getAttribute("src");
                var image = document.createElement('img');
                image.src = icon_src;
                image.className = "remove_icon";
                google.maps.event.addDomListener(image, 'click', function() {
                    removeRange(username);
                });

                var p = document.createElement('p');
                p.id = username;
                p.innerText = username;
                p.className = "user-label";
                p.appendChild(image);
                userSearchDiv.appendChild(p);
            }
        }

        var api =  {
            setCenter: function (position) {
                latitude = position.coords.latitude;
                longitude = position.coords.longitude;
                //map.setCenter({lat: latitude, lng: longitude});

                // selectedArea.setBounds(getDefaultBounds(latitude, longitude));
            },

            clearMap: function () {
                // remove previous markers from map and empty queriedUsersMarkers
                for (var key in marks) {
                    removeMark(key);
                }
            },

            plotUsers: function (users) {
                if(users !== null) {
                    for(var user in users) {
                        var tweetsFromUser = users[user];
                        for(var i = 0; i < tweetsFromUser.length; i++) {
                            api.plotTweet(tweetsFromUser[i]);
                        }
                    }
                }
            },

            plotTweets: function (tweets) {
                if(tweets != null) {
                    for (var i = 0; i < tweets.length; i++) {
                        api.plotTweet(tweets[i]);
                    }
                }
            },

            plotTweet: function (tweet) {
                var latJitter = Math.random() * .005 - .0025;
                var lngJitter = Math.random() * .005 - .0025;
                if(tweet != null && tweet["geo"] != null && tweet["geo"]["coordinates"] != null) {
                    var userGeoCoordData = tweet["geo"]["coordinates"];
                    var userMarker = new google.maps.Marker({
                        position: {lat: userGeoCoordData[0] + latJitter,
                                   lng: userGeoCoordData[1] + lngJitter},
                        map: map,
                        icon: redDotImg
                    });
                    var userText = "<b>" + tweet["user"]["screen_name"] + "</b>: " + tweet["text"]
                                 + "<br /> (" + prettyPrint(userGeoCoordData[0]) + ", "
                                 + prettyPrint(userGeoCoordData[1]) + ")";
                    attachTextToMarker(userMarker, userText);
                    google.maps.event.addListener(userMarker, 'mouseover', function() {
                        userMarker.setIcon(blueDotImg);
                    });
                    google.maps.event.addListener(userMarker, 'mouseout', function() {
                        userMarker.setIcon(redDotImg);
                    });
                    markers.push(userMarker);
                }
            },

            addRange: function(tweet_range) {
                var username = plotRange(tweet_range, true);
                console.log("addRange " + username);
                if (username !== null) {
                    addUserLabel(username);
                }
            },

            addRanges: function(tweet_ranges) {
                for (var i = 0; i < tweet_ranges.length; i++) {
                    var username = plotRange(tweet_ranges[i], false);
                    if (username !== null) {
                        addUserLabel(username);
                    }
                }
            },

            getSelectedArea: function () {
                return {ne_lat: selectedAreaNE.lat(),
                        ne_lng: selectedAreaNE.lng(),
                        sw_lat: selectedAreaSW.lat(),
                        sw_lng: selectedAreaSW.lng()
                };
            }
        };

        return api;
    };
});
