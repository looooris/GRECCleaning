import datetime

def openFile(fileName):
    file = open(fileName, 'r')
    lines = file.readlines()
    file.close()

    currentLine = lines[0]
    startOfData = 0
    while len(currentLine) != 13 and not (currentLine[0].strip().startswith('S0')):
        startOfData = startOfData + 1
        currentLine = lines[startOfData]
        
    lines = (lines[startOfData:-1])
    titles = lines[1]

    currentLine = lines[1]
    dataGap = 1
    while len(currentLine) != 13 and  not (currentLine[0].strip().startswith('S0')):
        dataGap = dataGap + 1
        currentLine = lines[dataGap]
    return lines, titles, dataGap

def setUpCSV(fileName, titles, firstData):
    headers = firstData[1][1:-1]
    headers = headers.split('","')
    subcategory = firstData[2]
    individualData = []
    for data in firstData[3:]:
        if data != '\n':
            individualData.append((data).split(','))
    
    ages = [ageRange[0].replace('"','') for ageRange in individualData]
    ages = str((ages*(len(headers)-1))).replace("'","")
    headers = ['"' + head + '"' + ',,,,,,' for head in headers[1:]]
    columns = len(headers)
    headers = (str(headers).replace("'",""))

    newFile = open(fileName + '.csv', 'w') 
    newFile.write('Ethnicity,' + headers[1:] + "\n")
    newFile.write('Age,' + ages[1:-1] + "\n")
    newFile.close()
    return columns

def writeData(data, fileName, gapLength, columns):
    currentData = data[0:gapLength]
    currentPosition = 0
    newFile = open(fileName + '.csv', 'a') 
    while len(currentData[0]) == 13 and currentData[0][1:-1].strip().startswith('S0'):
        lineToWrite = currentData[0].replace('"','').strip() + ','
        numericalData = []
        for tempData in currentData[3:10]:
            numericalData.append(tempData.split(','))
        for z in range(columns):
            lineToWrite = lineToWrite + numericalData[0][z+1] + ',' + numericalData[1][z+1] + ',' + numericalData[2][z+1] + ',' + numericalData[3][z+1] + ',' + numericalData[4][z+1] + ',' + numericalData[5][z+1] + ',' + numericalData[6][z+1] +','
        newFile.write(lineToWrite + "\n")
        currentPosition = currentPosition + gapLength
        currentData = data[currentPosition:currentPosition+gapLength]
    newFile.close()   
    print("All Done!") 


name = input("Please enter a file name: ")
outputFileName = name[:-4] + "_Cleaned{:%Y%m%d-%H:%M}".format(datetime.datetime.now())
splitLines, headerTitles, gapLength = openFile(name)
columns = setUpCSV(outputFileName, headerTitles, splitLines[0:gapLength])
writeData(splitLines, outputFileName, gapLength, columns)