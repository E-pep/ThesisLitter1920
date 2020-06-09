


def Queuer(indexFile):
  # Opening the Outputfile of the microcontroller

  PublishTimesList = []

  QueueTimesFile = "outputRpy"
  LogFile = "timings.log"
  SearchTimeAfter = "Received"


  with open(QueueTimesFile, 'r') as f:
    for line in f:
      line = line.replace("2020-05-19 ", "")
      line = line.replace(" Device 1 : Data published.","")
      line = line.replace("\r", "")
      line = line.replace("\n", "")
      line = line.replace(",", ".")
      print(line)
      PublishTimesList.append(line)



  #opening Timings.log to write extra column

  with open(LogFile, "r") as file:
    data = file.readlines()

    i = 0
    for line in data:
      tempLine = line
      tempLine = tempLine.replace(SearchTimeAfter, '  TimePublisher: ' + PublishTimesList[i] + ' 	 Received' )
      print(tempLine)
      data[i] = tempLine
      i+=1

  print(data)

  with open(LogFile, "w") as f2:
    f2.writelines( data )



if __name__ == "__main__":
    Queuer(1)
