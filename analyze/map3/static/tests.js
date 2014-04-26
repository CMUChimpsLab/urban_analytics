
test("hello world test", function() {
    ok(1=="1", "Passed!");
});

test("filterDates test", function() {
    var tweets = [{"name": "date1", "created_at": new Date(2013, 12, 31, 12, 59, 59)},
                {"name": "date2", "created_at": new Date(2014, 01, 01, 12, 00, 00)}]
    var noDates = filterDates(tweets, new Date(2014, 02, 02), new Date(2014, 02, 03));
    equal(noDates.length, 0, "These dates are should have no tweets between them.");

    var oneDate = filterDates(tweets, new Date(2014, 01, 01), new Date(2014, 01, 02));
    equal(oneDate.length, 1);
    equal(oneDate[0].name, "date2");

    var twoDates = filterDates(tweets, new Date(2000, 01, 01), new Date(2100, 01, 01));
    equal(twoDates.length, 2);
    
});

