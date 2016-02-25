import csv
from pylab import *

xx = []
yPos = []
yNeg = []
fi_Pos = plt.figure()
fi_Neg = plt.figure()
fi = plt.figure()

cnt = 0
def drawAnnotate():
    plt.xlabel('Time(s)')
    plt.ylabel('Sentiment analysis')

def drawGraph(last):
    print(last)

    ax1 = fi_Pos.add_subplot(111)
    axx1 = fi.add_subplot(111)
    ax2 = fi_Neg.add_subplot(111)
    axx2 = fi.add_subplot(111)

    ax1.plot(xx, yPos, color = 'g')
    axx1.plot(xx, yPos, color = 'g')
    ax2.plot(xx, yNeg, color = 'r')
    axx2.plot(xx, yNeg, color = 'r')

    yPos.clear()
    yNeg.clear()

def read_data_from_CSV_file():
    with open('Data/comment_data.csv','r',encoding='utf-8', errors='ignore') as csv_file:
        reader = csv.reader(csv_file, lineterminator='', delimiter=',')
        last = 'Post'
        for row in reader:
            if row[2] != last:
                if last != 'Post':
                    create_vector_to_cluster(20, last)
                    drawGraph(last)
                last = row[2]
                xx.clear()
                xx.append(row[0])
                yPos.append(row[4])
                yNeg.append(row[5])
            else:
                if last != 'Post':
                    xx.append(row[0])
                    yPos.append(row[4])
                    yNeg.append(row[5])

    drawAnnotate()
    show()

def convert_float(num):
    return float("{0:.4f}".format(num))

def getAverage(xtemp):
    sum = 0
    for x in xtemp:
        sum += float(x)
    return sum / len(xtemp)

def create_vector_to_cluster(cnt_period, topic):
    maxValue = int(xx[len(xx) - 1])
    dist = int(maxValue / cnt_period)
    vlast = dist
    xtemp = []
    pos_ = 0
    cc = 0
    myvector = []
    myvector.append(topic)
    for x in xx:
        if (int(x) <= vlast):
            xtemp.append(yNeg[pos_])
        else:
            averageX = getAverage(xtemp)
            myvector.append(convert_float(averageX))
            # print(convert_float(averageX), ' ', len(xtemp))
            xtemp.clear()
            xtemp.append(yNeg[pos_])
            vlast += dist
            cc += 1
        pos_ += 1
    for ii in range(cc + 1, cnt_period):
        myvector.append(myvector[len(myvector) - 1 ])

    import  csv
    with open('Data/vector_clustering_negative.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n', delimiter=',')
        writer.writerow(myvector)
    print(cc)
    print(myvector)

def read_data_vector_from_CSV_file(link):
    import  csv
    with open(link, 'r',encoding='utf-8', errors='ignore') as csv_file:
        reader = csv.reader(csv_file, lineterminator='', delimiter=',')
        xx.clear()
        for i in range(1, 21):
            xx.append(i)
        for row in reader:
            yPos.clear()
            yNeg.clear()
            for i in range(1, 21):
                yPos.append(row[i])
                yNeg.append(row[i])
                # print(row[i])
            drawGraph(row[0])
            # print(xx)
            # print(yPos)
    drawAnnotate()
    show()
# read_data_from_CSV_file()
read_data_vector_from_CSV_file('Data/vector_clustering_positive.csv')
