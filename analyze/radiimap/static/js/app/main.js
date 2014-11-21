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
    });
});
