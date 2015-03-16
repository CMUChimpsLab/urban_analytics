define(['jquery', 'app/TweetMap'], function ($, TweetMap) {
    $(document).ready(function () {
        var $body = $("body");
        var tweetMap = new TweetMap(document.getElementById('map-canvas'), document.getElementById("data-panel"));

        /**
         * Check if user allows geolocation, and center the map if so.
         */
        // if(navigator.geolocation) {
        //     navigator.geolocation.getCurrentPosition(function (position) {
        //         tweetMap.setCenter(position);
        //     }, function (msg) {
        //         console.log(typeof msg == 'string' ? msg : "error");
        //     });
        // }
        // else {
        //     alert("Geolocation is not supported or allowed on your browser.");
        // }

        // ajax setup
        $.ajaxSetup({
            beforeSend: function () {
                $body.addClass("loading");
            },
            complete: function () {
                $body.removeClass("loading");
            }
        });

        /**
         * Bind buttons
         */
        $("#get-all-tweets-btn").on("click", function () {
            $.ajax({
                type: "get",
                url: $SCRIPT_ROOT + "/get-all-tweets",
                success: function (response) {
                    tweetMap.clearMap();
                    tweetMap.plotTweets(response["tweets"]);
                },
                error: function () {
                    console.log("ajax request failed for " + this.url);
                }
            });
        });

        // $("#get-all-tweets-from-area-btn").on("click", function () {
        //     $.ajax({
        //         type: "get",
        //         data: tweetMap.getSelectedArea(),
        //         url: $SCRIPT_ROOT + "/get-all-tweets-from-area",
        //         success: function (response) {
        //             tweetMap.clearMap();
        //             tweetMap.plotTweets(response["tweets"]);
        //         },
        //         error: function () {
        //             console.log("ajax request failed for " + this.url);
        //         }
        //     });
        // });

        $("#get-user-tweets-btn").on("click", function () {
            $.ajax({
                type: "get",
                data: {user_screen_name: $("#user-screen-name-input").val()},
                url: $SCRIPT_ROOT + "/get-user-tweets",
                success: function (response) {
                    tweetMap.clearMap();
                    tweetMap.plotTweets(response["tweets"]);
                    // tweetMap.plotHome(response["user_home"]);
                    // tweetMap.plotPrediction(response["prediction"]);
                },
                error: function () {
                    console.log("ajax request failed for " + this.url);
                }
            });
        });

        // $("#get-user-tweets-from-area-btn").on("click", function () {
        //     $.ajax({
        //         type: "get",
        //         data: tweetMap.getSelectedArea(),
        //         url: $SCRIPT_ROOT + "/get-user-tweets-from-area",
        //         success: function (response) {
        //             tweetMap.clearMap();
        //             tweetMap.plotUsers(response["users"]);
        //         },
        //         error: function () {
        //             console.log("ajax request failed for " + this.url);
        //         }
        //     });
        // });
    });
});
