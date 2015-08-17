#!/usr/bin/python

import csv
from ParseTweet import *

tests_passed = tests_failed = 0
for line in csv.reader(open("tester-files/ParseTweet-tests.csv")):
	if line[0] == "number":
		returned = ParseTweet.get_one_number(line[1]) 
		returned = str(returned)
		if returned == '-1.0':
			returned = ParseTweet.check_for_missing_space(line[1])
			returned = str(returned)

	elif line[0] == "mc":
		returned = ParseTweet.get_one_letter(line[1])

	else:
		continue

	expected = line[2]
	if (returned == expected):
		tests_passed += 1
	else:
		tests_failed += 1
		print "This test failed for %s, expected %s, returned %s" % (line[1], line[2], returned)
print
print "Passed: " + str(tests_passed) 
print "Failed: " + str(tests_failed)


