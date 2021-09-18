import sys
import pandas as pd
import numpy as np
import math
sys.path.append('/Users/victorkaplan/Desktop/HackRice/HackRice11-OrderManagement/src/Database')
import database
from IPython.display import clear_output

#CURRENT VERSION****************

#code to read in from database:
def readin():
    workersdb = database.get_under_directory('/Workers')
    workers = pd.DataFrame.from_dict(workersdb, orient='index')
    workers = workers.reset_index()
    workers = workers.drop('index', axis=1)
    workers.head()

    equipdb = database.get_under_directory('/Equipments')
    equip = pd.DataFrame.from_dict(equipdb, orient='index')
    equip = equip.reset_index()
    equip = equip.drop('index', axis=1)
    equip.head()

    facildb = database.get_under_directory('/Facilities')
    facil = pd.DataFrame.from_dict(facildb, orient='index')
    facil = facil.reset_index()
    facil['workersIn']= facil['workersIn'].astype(int)
    facil['Maximum Occupacy']= facil['Maximum Occupacy'].astype(int)
    facil = facil.drop('index', axis=1)
    facil.head()

    workOrdersdb = database.get_under_directory('/WorkOrders')
    workOrders = pd.DataFrame.from_dict(workOrdersdb, orient='index')
    workOrders = workOrders.reset_index()
    workOrders['Priority(1-5)']= workOrders['Priority(1-5)'].astype(int)
    workOrders['Submission Timestamp'] = pd.to_datetime(workOrders['Submission Timestamp'])
    workOrders = workOrders.drop('index', axis=1)
    workOrders.head()
    return workers, equip, facil, workOrders

read = readin()
workers = read[0]
equip= read[1]
facil= read[2]
workOrders= read[3]

def priority(workOrderdf):
    realPriors = workOrderdf['Priority(1-5)']
    times = workOrderdf['Submission Timestamp']
    maxtime = max(times)
    timePrior = ([-(time - maxtime).days for time in times])
    final = (timePrior) + (realPriors)
    workOrderdf['newPrior'] = final
    return workOrderdf

workOrders = priority(workOrders)
workOrders.head()

#matching functions:
def dist(facilityloc1, facilityloc2):
    if facilityloc1 == facilityloc2:
        return 0
    return 2

def bid(workerdf, equipType, facility, timeToComplete, shift):
    df = workerdf.copy()
    df = df.loc[df['inTask'] == 'False']
    df = df.loc[df['Shifts'] == shift]
    df = df[df['Equipment Certification(s)'].str.contains(equipType,case=False)]
    final = []
    for i in df.index:
        final.append((i, dist(df.at[i, 'Loc'], facility) + int(timeToComplete)))
    return final

def pair(workerdf, workOrderdf, facilitydf, shift):
    sliceddf = workOrderdf.loc[workOrderdf['inProgress'] == 'False']
    currentJob = sliceddf['newPrior'].idxmax()
    print(list(sliceddf['newPrior']))
    print(currentJob)

    if int(facilitydf.loc[facilitydf['Facility'] == (workOrderdf.at[currentJob, 'Facility']), 'Maximum Occupacy']) <= int(facilitydf.loc[facilitydf['Facility'] == (workOrderdf.at[currentJob, 'Facility']), 'workersIn']):
        print('full')
        workOrderdf.at[currentJob, 'newPrior'] -= 1
        return None

    bids = bid(workerdf, workOrderdf.at[currentJob, 'Equipment Type'], workOrderdf.at[currentJob, 'Facility'], workOrderdf.at[currentJob, 'Time to Complete'], shift)
    lowest = math.inf
    lowestPair = None
    for bidPair in bids:
        if bidPair[1] < lowest:
            lowest = bidPair[1]
            lowestPair = bidPair
    if lowestPair != None:
        return (workerdf.at[lowestPair[0], 'Name'], workOrderdf.at[currentJob, 'Work Order ']), (lowestPair[0],currentJob), lowest
    workOrderdf.at[currentJob, 'newPrior'] -= 1
    return None

def update(pair, workerdf, workOrderdf, time, facilitydf):
    oldloc = list((facilitydf.loc[facilitydf['Facility'] == workerdf.at[pair[0], 'Loc']])['Facility'])[0]
    newloc = list((facilitydf.loc[facilitydf['Facility'] == workOrderdf.at[pair[1], 'Facility']])['Facility'])[0]
    oldlocinx = list(facilitydf.loc[facilitydf['Facility'] == oldloc].index)[0]
    newlocinx = list(facilitydf.loc[facilitydf['Facility'] == newloc].index)[0]

    facilitydf.at[oldlocinx, 'workersIn'] -= 1
    facilitydf.at[newlocinx, 'workersIn'] += 1

    workOrderdf.at[pair[1], 'inProgress'] = True
    workOrderdf.at[pair[1], 'timeLeft'] = time

    workerdf.at[pair[0], 'inTask'] = True
    workerdf.at[pair[0], 'Loc'] = newloc
    workerdf.at[pair[0], 'TasktimeLeft'] = time

def assignAll(workerdf, workOrderdf, facilitydf, shift):
    for i in range(len(workOrderdf.index)*2):
#         print(workerdf['inTast'])
#         print(False in list(workerdf['inTast']))
        if ('False' in list(workerdf['inTask'])):
            print(i)
            pair1 = pair(workerdf, workOrderdf, facilitydf, shift)
            if pair1 != None:
                update(pair1[1], workerdf, workOrderdf, pair1[2], facilitydf)

#write to db function:
def updatedb():
    workersName = workers.copy()
    workersName.index = workersName['Name']
    workersttodict = workersName.to_dict(orient = 'index')
    database.set_with_dict(workersttodict, '/Workers')

    workOrdersName = workOrders.copy()
    workOrdersName['Submission Timestamp'] = workOrdersName['Submission Timestamp'].astype(str)
    workOrdersName.index = workOrdersName['Work Order ']
    workOrdersNametodict = workOrdersName.to_dict(orient = 'index')
    database.set_with_dict(workOrdersNametodict, '/WorkOrders')

    facilName = facil.copy()
    facilName.index = facilName['Facility']
    facilNametodict = facilName.to_dict(orient = 'index')
    database.set_with_dict(facilNametodict, '/Facilities')

    return None
