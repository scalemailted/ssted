import csv
from collections import defaultdict
#from datetime import datetime
import datetime

def readFile():
    csv_file = open('sx-mathoverflow-a2q.txt', 'r')
    #sx_data = [ row.split(' ') for row in sx_file.readlines()]
    sx_data = [ tuple(sorted(map(int,row))) for row in csv.reader(csv_file, delimiter=' ')]
    return sx_data

def generateEdgelist(data):
    edgeList = defaultdict(lambda: [])
    for row in data:
        n1, n2, ts = row
        #ts = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        ts = datetime.datetime.fromtimestamp(ts)
        edgeList[(n1,n2)].append(ts)
    return edgeList

def generateDuplicates(edgeList):
    duplicates = {}
    for edge in edgeList:
        if len(edgeList[edge]) > 1:
            duplicates[edge] = edgeList[edge]
    return duplicates

def generateDiffs(duplicates):
    differences = defaultdict(lambda: [])
    for edge in duplicates:
        for i in range(len(duplicates[edge])-1):
            time = duplicates[edge][i+1] - duplicates[edge][i]
            differences[edge].append(time)
    return differences




def filterByYear(data, year):
    year_data = defaultdict(lambda: [])
    for edge in data:
        filtered = [ date for date in data[edge] if date.year == year]
        if len(filtered) > 1:
            year_data[edge] = filtered
        #for date in data[edge]:
        #    if date.year == year:
        #        year_data[edge].append(date)
    return year_data

def filterByMonth(data, year, month):
    month_data = defaultdict(lambda: [])
    year_data = filterByYear(data, year)
    for edge in year_data:
        filtered = [ date for date in year_data[edge] if date.month == month]
        if len(filtered) > 1:
            month_data[edge] = filtered
        #for date in data[edge]:
        #    if date.year == year:
        #        year_data[edge].append(date)
    return month_data


def calculateTotalOccurences(edgelist):
    count = 0
    for edge in edgelist:
        count += len(edgelist[edge])
    return count

def getTotalOccurences(edgelist):
    occurences = []
    for edge in edgelist:
        count = len(edgelist[edge])
        occurences.append(count)
    return sorted(occurences)

def getFrequencies(occurences):
    frequencies = {};
    for count in set(occurences):
        frequencies[count] = occurences.count(count)
    return frequencies 



data = readFile()
edgelist = generateEdgelist(data)       #edgelist of stackoverflow data
dupes = generateDuplicates(edgelist)    #dupes from stackoverflow data
diffs = generateDiffs(dupes)            #differences in time for repeated edges
sumOccurences = calculateTotalOccurences(edgelist)   #sum of all occurences for each unique edge, should equal total rows
occurences = getTotalOccurences(edgelist)            #get count of occurences for each edge (to plot at line graph)
frequencies = getFrequencies(occurences)             #get frequency for each occurence


import matplotlib.pyplot as plt
#Total occurences
plt.plot( list(frequencies.keys()), list(frequencies.values()))
plt.show()

#Repeated occurences
plt.plot( list(frequencies.keys())[1:], list(frequencies.values())[1:])
plt.show()

#Filter by year/month
years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]
yearly_reoccurences = []
for year in years:
    count = len(filterByYear(dupes, year))
    yearly_reoccurences.append(count)
plt.plot(years, yearly_reoccurences)
plt.show()


months = [1,2,3,4,5,6,7,8,9,10,11,12]
monthly_reoccurences = []
xaxis = []
for year in years:
    for month in months:
        count = len(filterByMonth(dupes, year, month))
        monthly_reoccurences.append(count)
        xaxis.append(str(month)+'-' +str(year))
plt.plot(xaxis, monthly_reoccurences)
plt.xticks(xaxis, xaxis, rotation=45, fontsize=6)          # You can specify a rotation for the tick labels in degrees or with keywords.
plt.subplots_adjust(bottom=0.15)
plt.show()


def plotTimeDeltas(diffs):
    counter = 0;
    for deltaArray in diffs.values():
        counter+=1;
        xaxis = [ dt.total_seconds() for dt in  deltaArray ]
        yaxis = [ counter ] * len(xaxis)
        plt.plot( xaxis, yaxis, 'o')
    plt.show()


def generateUnixList(data):
    edgeList = defaultdict(lambda: [])
    for row in data:
        n1, n2, ts = row
        edgeList[(n1,n2)].append(ts)
    return edgeList


def plotUnixTime(unixList):
    counter = 0;
    for timeArray in unixList.values():
        counter+=1;
        xaxis = timeArray
        yaxis = [ counter ] * len(timeArray)
        print('xaxis: ' + str(len(timeArray)) + ', yaxis: '+str(len(yaxis)) )
        plt.plot( xaxis, yaxis, 'o')
    plt.show()


unixList = generateUnixList(data)
plotUnixTime(unixList)