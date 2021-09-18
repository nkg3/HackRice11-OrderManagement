import sys
sys.path.append('C:/Users/justi/Desktop/Hackathon/HackRice11-OrderManagement/src/Database')
import database

database.init_database("https://hackrice11-ordermanageme-327b0-default-rtdb.firebaseio.com", "../DataFiles/database_private_key.json")
bigdic = database.get_under_directory("/Facilities")
# Look up coordinates for Fac1, Fac2, Fac3, Fac4, Fac5
iter = range(len(bigdic))
coordinates = []
for num in iter:
    coordinates.append(bigdic['Fac'+str(num+1)]['Latitude'])
    coordinates.append(bigdic['Fac'+str(num+1)]['Longitude'])
    num += 1

print(coordinates)