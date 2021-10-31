from os import times
import matplotlib.pyplot as plt
import csv

def plotCwnd(statsPath, algName):
    timestamp = []
    cwnd = []

    with open(statsPath, mode = 'r') as csvFile:
        rows = csv.DictReader(csvFile)
        for content in rows:
            timestamp.append(float(content["Timestamp"]))
            cwnd.append(int(content["cwnd"]))

    # map timestamps to start with 0
    firstTimestamp = timestamp[0]
    for i in range(len(timestamp)):
        timestamp[i] -= firstTimestamp

    plt.plot(timestamp, cwnd)
    # plt.xticks(np.arange(3, 51, 5.0))
    plt.xlabel('Timestamp')
    plt.ylabel('CWND')
    plt.title(algName)
    plt.show()


algorithmNames = ['reno', 'vegas', 'bic', 'cubic']

algName = algorithmNames[3]
statsFilePath = 'ex1/socket_stats_' + algName + '.csv'
plotCwnd(statsFilePath, algName)