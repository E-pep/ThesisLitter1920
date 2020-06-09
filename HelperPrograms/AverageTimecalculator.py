import os
import re
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime
from datetime import timedelta
import csv

# time_str = '17:10:00.058217'
# time_str2 = '17:10:00.000007'
# time_object = datetime.strptime(time_str, '%H:%M:%S.%f')
# time_object2 = datetime.strptime(time_str2, '%H:%M:%S.%f')
# print(type(time_object))
# print(time_object)

# time_object2 = time_object-time_object2
# print(time_object2)

def ReadData(indexFile):
    logfile = indexFile
    FirstTimestamp = "AfterReadIn"

    TimestampsNameList = []
    TimestampsTimeList = []


    with open(logfile) as lines:
        lines = lines.readlines()

    for line in lines:
        print(line)
        if "Compile it manually" not in line and "SecondModel" not in line:
            line = line[line.find(FirstTimestamp):]
            TimestampStrings = re.split(r'\t+', line.rstrip('\t'))


            # collect the times and put them in temperary list. Push them into final list.
            TempTimestampList = []
            for TimestampString in TimestampStrings:
                print("Timestampstring = " + TimestampString)
                print(re.split(r': +', TimestampString)[1])
                TempTimestampList.append((re.split(r': ', TimestampString)[1]).strip('\n').replace('2020-05-19 ', '').replace('+02:00', '').replace(' ', ''))
            TimestampsTimeList.append(TempTimestampList)





    # Collect timestamp names
    for TimestampString in TimestampStrings:
        test = re.split(r':+', TimestampString)[0]
        TimestampsNameList.append(test.strip(' '))

    print('Nameslist:')
    print(TimestampsNameList)
    # print(TimestampsTimeList[0][1])

    # calculate average time between every timestamp

    averageTimesList = [timedelta(0)] * (len(TimestampsNameList) - 1)

    for Timingslist in TimestampsTimeList:
        # print(Timingslist)
        for index in range(0,(len(Timingslist) -1)):

            time1 = datetime.strptime(Timingslist[(index + 1)], '%H:%M:%S.%f')
            time2 = datetime.strptime(Timingslist[index], '%H:%M:%S.%f')
            averageTimesList[index] = (time1 - time2) + averageTimesList[index]



    # calculate mean average
    for index in range(0, len(averageTimesList)):
        averageTimesList[index] = averageTimesList[index] / len(TimestampsTimeList)

    # List that contains values that are plotted because seconds at up to eachothers
    averageTimesListAdded = []
    averageTimesListAdded.append(timedelta(0))

    for index in range(0, len(averageTimesList)):
        averageTimesListAdded.append((averageTimesListAdded[index] + averageTimesList[index]))


    #convert to string:

    # convert averageTimesList
    for index in range(0, len(averageTimesList)):
        averageTimesList[index] = str(averageTimesList[index])

    #convert Added
    for index in range(0, len(averageTimesListAdded)):
        averageTimesListAdded[index] = str( averageTimesListAdded[index] )

    print('averageTimesList:')
    print(averageTimesList)
    averageTimesListAdded[0] = averageTimesListAdded[0] + '.00'
    print('averageTimesListAdded:')
    print(averageTimesListAdded)

    averageTimesListAddedDatetime = [datetime.strptime(d, "%H:%M:%S.%f") for d in averageTimesListAdded]
    print('averageTimesListAddedDatetime:')
    print(averageTimesListAddedDatetime)

    # plot on timeline

    # calculate total time needed for the 40 pictures
    first_time = datetime.strptime(TimestampsTimeList[0][0], '%H:%M:%S.%f')
    last_time = datetime.strptime(TimestampsTimeList[(len(TimestampsTimeList) -1)][(len(TimestampStrings) -1)], '%H:%M:%S.%f')
    total_time = last_time - first_time
    print('total time for the 40 pictures:')
    print(total_time)


    # Write everything away to csv file

    with open('MultipleUsers_10Users_Averages.csv', 'a+', newline='') as file:
        writer = csv.writer(file)
        naam = "split" + str(indexFile)
        writer.writerow([naam, TimestampsNameList, averageTimesList, averageTimesListAdded, averageTimesListAddedDatetime, total_time])

    print(indexFile)

if __name__ == "__main__":
    ReadData("timings.log")