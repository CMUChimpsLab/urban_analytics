#!/usr/bin/env python
# From http://www.johndcook.com/python_longitude_latitude.html

import math

# Returns the distance between 2 points in meters, based on a spherical earth.
# Sphere earth radius = 6371 km, from http://en.wikipedia.org/wiki/Earth_radius
def earth_distance_m(lat1, long1, lat2, long2):
    return distance_on_unit_sphere(lat1, long2, lat2, long2) * 6371 * 1000

# Returns the distance between two points, based on a spherical earth, in units
# of "earth radii".
def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + \
           math.cos(phi1)*math.cos(phi2))
    if cos > 1.0:
        cos = 1.0 # I guess in cases of very close points it becomes 1.000001?
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc
