import googlemaps

#Perform request to use the Google Maps API web service
API_key = 'AIzaSyB49WzrgV2c2ly9IOTsZOmsXnQuWC9DGPI'
gmaps = googlemaps.Client(key=API_key)

from itertools import tee
import database


database.init_database("https://hackrice11-ordermanageme-327b0-default-rtdb.firebaseio.com", "./DataFiles/database_private_key.json")
fac_info = database.get_under_directory("/Facilities")

# Look up coordinates for Fac1, Fac2, Fac3, Fac4, Fac5
iter = range(len(fac_info))
coordinates = []
for num in iter:
    coordinates.append(fac_info['Fac'+str(num+1)]['Latitude'])
    coordinates.append(fac_info['Fac'+str(num+1)]['Longitude'])
    num += 1

coordinates_float = []
# Convert string to float
for num in range(len(coordinates)):
    coordinates_float.append((float(coordinates[num])))
    num += 1

# Separate coordinates to different facility lists
fac1 = []
fac2 = []
fac3 = []
fac4 = []
fac5 = []

for num in range(2):
    fac1.append(coordinates_float[num])
    fac2.append(coordinates_float[num+2])
    fac3.append(coordinates_float[num+4])
    fac4.append(coordinates_float[num+6])
    fac5.append(coordinates_float[num+8])

def distance_result(originfac,destfac):
    """
    Finds the distance and the time it takes to drive from one facility to another

    Inputs:
      originfac - the coordinates (latitude, longitude) of the origin
      destfac - the coordinates (latitude, longitude) of the destination

    Returns a list representing distance and duration of trip
    """
    # converts list to tuple
    origins = tuple(originfac)
    destinations = tuple(destfac)

    #empty list - will be used to store calculated distances and time
    list = []
    
    #pass origin and destination variables to distance_matrix function# output in meters
    distance = gmaps.distance_matrix(origins, destinations, mode='driving')["rows"][0]["elements"][0]["distance"]["text"]
    time = gmaps.distance_matrix(origins, destinations, mode='driving')["rows"][0]["elements"][0]["duration"]["text"]
    #append distance and time to list
    list.append(distance)
    list.append(time)
    # returns a list with distance and duration of trip
    return list

print(distance_result(fac1,fac2))
