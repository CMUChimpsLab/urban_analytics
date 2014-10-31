#!/usr/bin/env python

# Takes people's responses to the recruitment form and geocodes them so we have
# a latitude-longitude pair.

from pygeocoder import Geocoder

results = Geocoder.geocode("Tian'anmen, Beijing")

print results
