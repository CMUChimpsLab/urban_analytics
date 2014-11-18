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
        var centerMarker;
        var queriedUsersMarkers = [];
        var redDotImg = 'static/images/maps_measle_red.png';
        var blueDotImg = 'static/images/maps_measle_blue.png';
        var mapOptions = {
            center: {lat: latitude, lng: longitude},
            zoom: 14,
            disableDefaultUI: true
        };
        var map = new google.maps.Map(canvas, mapOptions);

        // Define the rectangle.
        var selectedAreaNE,
            selectedAreaSW;
        var selectedArea = new google.maps.Rectangle({
            bounds: getDefaultBounds(latitude, longitude),
            editable: true,
            draggable: true
        });
        // Put the rectangle on our map, I guess?
        selectedArea.setMap(map);
        google.maps.event.addListener(selectedArea, 'bounds_changed', updateDataPanel);
        updateDataPanel();

        // get the default bounds for a google.maps.Rectangle
        function getDefaultBounds(latitude, longitude) {
            return new google.maps.LatLngBounds(
                new google.maps.LatLng(latitude - 0.002, longitude - 0.004),
                new google.maps.LatLng(latitude + 0.002, longitude + 0.004)
            );
        }

        function updateDataPanel() {
            selectedAreaNE = selectedArea.getBounds().getNorthEast();
            selectedAreaSW = selectedArea.getBounds().getSouthWest();
            var contentString = '<b>NorthEast Corner:</b> ' + prettyPrint(selectedAreaNE.lat()) + ', ' + prettyPrint(selectedAreaNE.lng()) + '<br>' +
                '<b>SouthWest Corner:</b> ' + prettyPrint(selectedAreaSW.lat()) + ', ' + prettyPrint(selectedAreaSW.lng());

            dataPanel.innerHTML = contentString;
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

        var api =  {
            setCenter: function (position) {
                latitude = position.coords.latitude;
                longitude = position.coords.longitude;
                map.setCenter({lat: latitude, lng: longitude});

                centerMarker = new google.maps.Marker({
                    position: map.getCenter(),
                    map: map,
                    animation: google.maps.Animation.DROP,
                    title: 'Center of Map'
                });
                google.maps.event.addListener(centerMarker, 'click', function () {
                    map.setCenter(centerMarker.getPosition());
                });

                selectedArea.setBounds(getDefaultBounds(latitude, longitude));
            },

            clearMap: function () {
                // remove previous markers from map and empty queriedUsersMarkers
                if(queriedUsersMarkers.length > 0) {
                    for(var i = 0; i < queriedUsersMarkers.length; i++) {
                        queriedUsersMarkers[i].setMap(null);
                    }
                    queriedUsersMarkers.length = 0;
                }
            },

            plotUsers: function (users) {
                if(users != null) {
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
                    queriedUsersMarkers.push(userMarker);
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
