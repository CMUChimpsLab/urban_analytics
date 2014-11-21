define(['jquery', 'app/TweetMap'], function ($, TweetMap) {
    $(document).ready(function () {
        var $body = $("body");
        var tweetMap = new TweetMap(document.getElementById('map-canvas'), document.getElementById("data-panel"));

        /**
         * Check if user allows geolocation, and center the map if so.
         */
        if(navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                tweetMap.setCenter(position);
            }, function (msg) {
                console.log(typeof msg == 'string' ? msg : "error");
            });
        }
        else {
            alert("Geolocation is not supported or allowed on your browser.");
        }

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
        $("#get-user-tweet-range-btn").on("click", function () {
            $.ajax({
                type: "get",
                data: {user_screen_name: $("#user-screen-name-input").val()},
                url: $SCRIPT_ROOT + "/get-user-tweet-range",
                success: function (response) {
                    tweetMap.clearMap();
                    tweetMap.plotRange(response["tweet_range"]);
                },
                error: function () {
                    console.log("ajax request failed for " + this.url);
                }
            });
        });
        $("#user-screen-name-input").keyup(function(event){
            if(event.keyCode == 13){
                $("#get-user-tweet-range-btn").click();
            }   
        });
    });
});
