from datetime import datetime

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
import ast


# Read in CSV file
ModelNames = []
TimestampsNameList = []
TimestampsTimeList = []
averageTimesList = []



with open('MultipleUsers_10Users_Averages.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            ModelNames.append(row[0])
            TimestampsNameList.append(ast.literal_eval(row[1]))
            averageTimesList.append(ast.literal_eval(row[2]))
            line_count += 1
    print(f'Processed {line_count} lines.')

# [naam, TimestampsNameList, averageTimesList, averageTimesListAdded, averageTimesListAddedDatetime, total_time]



print(ModelNames)
print(TimestampsNameList)
print(TimestampsTimeList)
print(averageTimesList)

# Add zeros in

ImageEncode = []
PredictionEdgeSide = []
TimeInWaitingQueue = []
SendOver = []
PredictionCloudSide = []


# fill the ImageEncodelist
time_str = '00:00:00.000000'
time_object = datetime.strptime(time_str, '%H:%M:%S.%f')

ImageEncode.append((averageTimesList[0][0]).replace('0:00:', ''))
ImageEncode.append(averageTimesList[1][0].replace('0:00:', ''))
ImageEncode = (ImageEncode + ['00.000000'] * (len(ModelNames)))[:(len(ModelNames))]
print('Imageencode:')
print(ImageEncode)


# fill the PredictionEdgeSide
PredictionEdgeSide.append('00.000000')
PredictionEdgeSide.append('00.000000')
for i in range (2, len(averageTimesList)):
    PredictionEdgeSide.append(averageTimesList[i][0].replace('0:00:', ''))

print('PredictionEdgeSide:')
print(PredictionEdgeSide)

#fill in TimeInWaitingQueue
for i in range (0, len(averageTimesList)):
    TimeInWaitingQueue.append(averageTimesList[i][1].replace('0:00:', ''))

print('TimeInWaitingQueue:')
print(TimeInWaitingQueue)

# fill in sendover
for i in range (0, len(averageTimesList)):
    SendOver.append(averageTimesList[i][2].replace('0:00:', ''))

print('SendOver:')
print(SendOver)

# fill in PredictionCloudSide
PredictionCloudSide.append(averageTimesList[0][3].replace('0:00:', ''))
PredictionCloudSide.append(averageTimesList[1][3].replace('0:00:', ''))
PredictionCloudSide.append('00.000000')
for i in range (3, len(averageTimesList)):
    PredictionCloudSide.append(averageTimesList[i][3].replace('0:00:', ''))

print('PredictionCloudSide:')
print(PredictionCloudSide)


print('lengtes:')
print(len(ImageEncode))
print(len(PredictionEdgeSide))
print(len(SendOver))
print(len(PredictionCloudSide))

# wegschrijven naar csv en daar een chart maken (stomme matplotlib)

with open('MultipleUsers_10UsersBarChartt.csv', mode='w') as barfile:
    employee_writer = csv.writer(barfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    employee_writer.writerow(['Model', 'ImageEncode', 'PredictionEdgeSide', 'TimeInWaitingQueue', 'SendOver', 'PredictionCloudSide'])

    for times in range (0, len(averageTimesList)):
        employee_writer.writerow([ModelNames[times], ImageEncode[times], PredictionEdgeSide[times], TimeInWaitingQueue[times], SendOver[times], PredictionCloudSide[times]])



