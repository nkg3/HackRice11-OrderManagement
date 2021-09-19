import googlemaps

#Perform request to use the Google Maps API web service
API_key = 'AIzaSyB49WzrgV2c2ly9IOTsZOmsXnQuWC9DGPI'
gmaps = googlemaps.Client(key=API_key)

from itertools import tee
import sys
sys.path.append('C:/Users/justi/Desktop/Hackathon/HackRice11-OrderManagement/src/Database')
from . import database


# #database.init_database("https://hackrice11-ordermanageme-327b0-default-rtdb.firebaseio.com", "./DataFiles/database_private_key.json")
# fac_info = database.get_under_directory("/Facilities")

# # Look up coordinates for Fac1, Fac2, Fac3, Fac4, Fac5
# iter = range(len(fac_info))
# coordinates = []
# for num in iter:
#     coordinates.append(fac_info['Fac'+str(num+1)]['Latitude'])
#     coordinates.append(fac_info['Fac'+str(num+1)]['Longitude'])
#     num += 1

# coordinates_float = []
# # Convert string to float
# for num in range(len(coordinates)):
#     coordinates_float.append((float(coordinates[num])))
#     num += 1

# # Separate coordinates to different facility lists
# fac1 = []
# fac2 = []
# fac3 = []
# fac4 = []
# fac5 = []

# for num in range(2):
#     fac1.append(coordinates_float[num])
#     fac2.append(coordinates_float[num+2])
#     fac3.append(coordinates_float[num+4])
#     fac4.append(coordinates_float[num+6])
#     fac5.append(coordinates_float[num+8])

def distance_result(originfac,destfac):
    """
    Finds the distance and the time it takes to travel from one facility to another

    Inputs:
      originfac - the coordinates (latitude, longitude) of the origin
      destfac - the coordinates (latitude, longitude) of the destination
    """
    # converts list to tuple
    origin = tuple(originfac)
    destination = tuple(destfac)

    #empty list - will be used to store calculated distances
    list = [0]
    
    #pass origin and destination variables to distance_matrix function# output in meters
    result = gmaps.distance_matrix(origin, destination, mode='driving')["rows"][0]["elements"][0]["distance"]["value"]

    #append result to list
    list.append(result)
    return list

# print(distance_result(fac1,fac3))
