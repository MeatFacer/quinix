import csv
from collections import Counter
import datetime
from statistics import mean

def countTypes():
    amountOfLoadTypes = 4
    loadTypeSectionStart = 5
    vesselTypeIndex = 4
    vesselLoadOccurences = {1: [0] * 4, 2: [0] * 4, 3: [0] * 4, 4: [0] * 4, 5: [0] * 4}
    with open('VesselData.csv') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader, None)
        for row in reader:
            vesselType = int(row[vesselTypeIndex])
            for i in range(amountOfLoadTypes):
                if int(row[loadTypeSectionStart + 2*i]) != 0 or int(row[loadTypeSectionStart + 2*i + 1]) != 0:
                    vesselLoadOccurences[vesselType][i] += 1
    print(vesselLoadOccurences)

    """
    Result : {1: [0, 0, 0, 0], 2: [117, 112, 0, 12], 3: [60, 21, 0, 22], 4: [0, 0, 0, 0], 5: [0, 0, 385, 891]}
    Vesseltype 1 and 4 do not load or discharge anything in our dataset, therefore we can not conclude anything for those types by counting the occurences.
    We can see that vesseltype 2 mainly transports cargo type 1 and 2, vesseltype 3 does mainly 1 but also 2 and 4.
    We see that vesseltype 5 is the only type that moves cargo type 3 and does by far the most of cargo type 4
    """

def stevedoreCorralation():
    """
    find a correlation between stevedaores and cargo types
    """
    amountOfLoadTypes = 4
    loadTypeSectionStart = 5
    stevedoreIndex = 13
    stevedoreOccurances = {1: [], 2: [], 3: [], 4: []}
    with open('VesselData.csv') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader, None)
        for row in reader:
            for i in range(amountOfLoadTypes):
                if int(row[loadTypeSectionStart + 2*i]) != 0 or int(row[loadTypeSectionStart + 2*i + 1]) != 0:
                    stevedores = row[stevedoreIndex].split(',')
                    for stevedore in stevedores:
                        if(stevedore == ""):
                            continue
                        stevedoreOccurances[i + 1].append(int(stevedore[10:]))

    for i in range(amountOfLoadTypes):
        print(Counter(stevedoreOccurances[i]))

    """
    Result :
        Counter({61: 63, 67: 42, 56: 30, 77: 24, 89: 10, 66: 7, 26: 5, 74: 4, 75: 4, 100: 2, 65: 2, 45: 1, 43: 1, 94: 1})
        Counter({67: 76, 61: 27, 65: 13, 60: 12, 89: 6, 75: 4, 26: 3, 68: 2, 74: 2, 45: 1, 53: 1, 34: 1})
        Counter({107: 110, 83: 104, 84: 85, 104: 59, 89: 36, 114: 32, 35: 22, 23: 14, 7: 7, 75: 5, 15: 5, 19: 3, 3: 3, 78: 2, 101: 2, 110: 1, 73: 1, 38: 1, 64: 1})
        Counter({114: 186, 78: 143, 104: 121, 59: 121, 35: 94, 75: 87, 89: 70, 62: 64, 112: 50, 103: 43, 65: 33, 90: 27, 88: 24, 79: 23, 101: 20, 73: 19, 23: 19, 63: 17, 41: 17, 107: 15, 74: 8, 34: 8, 12: 8, 7: 7, 115: 6, 45: 6, 83: 6, 50: 5, 81: 5, 15: 5, 102: 4, 61: 4, 3: 4, 48: 4, 95: 4, 19: 3, 113: 2, 49: 2, 124: 2, 47: 2, 9: 2, 84: 2, 64: 2, 52: 1, 76: 1, 87: 1, 16: 1, 106: 1, 26: 1, 60: 1, 91: 1, 97: 1})
    
    Conclusion/guess:
        there seems to be some similarities between cargo types 1 and 2 and the names of the stevedores.
        Same goes for cargo types 3 and 4
        Should probably use percentages for the amount of times the cargo is present in our dataset vs the amount of times that cargo is handled by a certain stevedore  
    """

def timeInPort():
    amountOfLoadTypes = 4
    loadTypeSectionStart = 5
    arrivaltimeIndex = 1
    departuretimeIndex = 2
    timeOccurances = {1: [], 2: [], 3: [], 4: []}
    with open('VesselData.csv') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader, None)
        for row in reader:
            for i in range(amountOfLoadTypes):
                if int(row[loadTypeSectionStart + 2*i]) != 0 or int(row[loadTypeSectionStart + 2*i + 1]) != 0:
                    arrivalTime = datetime.datetime.strptime(row[arrivaltimeIndex][:-3], '%Y-%m-%d %H:%M:%S')
                    departureTime = datetime.datetime.strptime(row[departuretimeIndex][:-3], '%Y-%m-%d %H:%M:%S')
                    idleTime = departureTime - arrivalTime
                    timeOccurances[i + 1].append(idleTime.total_seconds())

    for i in range(amountOfLoadTypes):
        print("cargo type: ", i + 1, mean(timeOccurances[i + 1]))

    """
    Result:
    cargo type:  1 309966.10169491527
    cargo type:  2 253353.38345864663
    cargo type:  3 168311.6883116883
    cargo type:  4 202876.54054054053
    
    We can see some differences in the mean time that a vessel is in a port and the observed cargo type.
    As further analysis we could analyse the amount of load/discharge versus time
    """




"""
Obeservations based on excel:
isremakrable only contains false -> probrably useless info
same for hasnohamis
Most ships only move 1 type of cargo


General idea:
find correlation between known information and observed cargo types.
If we find a high correlation between certain input, or combinations of inputs and observed cargo types we can make an accurate prediction.
Possible correlations:
    -vesseltype
    -time in port -> difference between departure and arrival times
    -port origin/next port
    -assigned stevedores
    -amount of dwt


General observation:
A lot of our data has none of the cargo types we are looking for -> therefore we should look for correlations which do hold for when our cargo types are present, 
but which do not hold when there are none of our 4 cargo types present


ALL OF THIS iS QUITE BAD -> It was probably better to try to implement a model such as k-nearest neighbour
An AI model would probably work well here
K-nearest neighbour or regression could work


"""

timeInPort()