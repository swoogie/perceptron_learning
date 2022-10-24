import random
from parso import split_lines


def parseCancerData():
    readFile = open("breast_cancer.txt", "r")
    cancerData = readFile.read()
    readFile.close()
    cancerData = split_lines(cancerData)
    toBeRemoved = []
    for index, line in enumerate(cancerData):
        line = line.split(',', 1)[1]
        if (line[-1] == '2'):
            line = line[:-1] + '0'
        else:
            line = line[:-1] + '1'
        cancerData[index] = line

        for digit in line.split(','):
            try:
                int(digit)
            except:
                toBeRemoved += [index]
                break

    for index in reversed(toBeRemoved):
        cancerData.pop(index)

    writeFile = open("cancer_new.txt", "w")
    for line in cancerData:
        writeFile.write(line + "\n")

    writeFile.close()


def parseIrisData():
    irisData = open("iris.txt")
    irisData = irisData.read()
    irisData = split_lines(irisData)

    for index, line in reversed(list(enumerate(irisData))):
        line = line.split(',')

        if (line[-1] == "Iris-versicolor"):
            line[-1] = '0'
            irisData[index] = ''
            for digit in line:
                irisData[index] += digit + ','
            irisData[index] = irisData[index][:-1] + ''
        elif (line[-1] == "Iris-virginica"):
            line[-1] = '1'
            irisData[index] = ''
            for digit in line:
                irisData[index] += digit + ','
            irisData[index] = irisData[index][:-1] + ''
        else:
            irisData.pop(index)

    random.shuffle(irisData)

    writeFile = open("iris_new.txt", "w")
    for line in irisData:
        writeFile.write(line + '\n')

    writeFile.close()


def main():
    parseCancerData()
    parseIrisData()


if __name__ == "__main__":
    main()
