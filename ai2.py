from fileinput import filename
from multiprocessing.sharedctypes import Value
import random
from parso import split_lines
import math
import matplotlib.pyplot as plt
import numpy as np

EPOCHS = 100
LEARN_TEST_RATIO = 0.7
RANDOM_WEIGHT = 0.123123
LEARN_RATE = 0.001


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


def getFileData(fileName):
    readFile = open(fileName)
    fileData = readFile.read()
    readFile.close()
    fileData = split_lines(fileData)
    length = len(fileData)
    index = round(LEARN_TEST_RATIO * length)
    return fileData[:index], fileData[index:-1]


def parseLineData(line):
    line = str(line).split(',')
    t = float(line[-1])
    x = [1]
    for digit in range(len(line) - 1):
        x.append(float(line[digit]))
    return x, t


def calculateA(x, w):
    a = 0
    for i in range(len(x)):
        a += float(x[i]) * float(w[i])
    return a


def stepFunction(a):
    if (a >= 0):
        return 1
    else:
        return 0


def sigmoidFunction(a):
    return (1 / (1 + math.exp(-a)))  # e^-a


def calculateAdaline(w, x, t, y, learnRate):
    newW = []
    for index, weight in enumerate(w):
        newW.append(round(float(weight) + learnRate *
                    (float(t) - float(y)) * float(x[index]), 4))
    return newW


def testingPhase(w, testData, aFunc):
    count = 0
    cost = 0
    for line in testData:
        x, t = parseLineData(line)
        a = calculateA(x, w)
        if (aFunc == 0):
            y = stepFunction(a)
        else:
            y = sigmoidFunction(a)
        if (round(y) == int(t)):
            count += 1
        else:
            cost += pow(y - t, 2)
    return ((count / len(testData)) * 100), round(cost, 3)


def learningPhase(weights, learnData, aFunc, learnRate):
    for line in learnData:
        x, t = parseLineData(line)
        a = calculateA(x, weights)
        if (aFunc == 0):
            y = stepFunction(a)
        else:
            y = sigmoidFunction(a)
        if (y != t):
            weights = calculateAdaline(weights, x, t, y, learnRate)
    return weights


def learningAndTesting(learnData, testData, aFunc, learnRate, useTestData):
    positives = []
    cost = []
    weights = []
    for _ in str(learnData[0]).split(','):
        weights.append(RANDOM_WEIGHT)

    for _ in range(EPOCHS):
        weights = learningPhase(weights, learnData, aFunc, learnRate)
        if useTestData:
            positive, err = testingPhase(weights, testData, aFunc)
        else:
            positive, err = testingPhase(weights, learnData, aFunc)
        positives.append(positive)
        cost.append(err)
    return positives, cost, weights


def plot(val, ylabel):
    x = np.arange(0, EPOCHS)
    y = val

    fig, ax = plt.subplots()

    ax.set_ylim(ymin=0, ymax=100)
    ax.set_xlim(xmin=0, xmax=100)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Epoch index")
    ax.plot(x, y)

    plt.show()


def main():
    parseCancerData()
    parseIrisData()
    fileNames = ["iris_new.txt", "cancer_new.txt"]
    useTestData = [True, False]
    for fileName in fileNames:
        learnData, testData = getFileData(fileName)
        print(f"Using file {fileName}")
        for i in range(2):
            for use in useTestData:
                positives, cost, w = learningAndTesting(
                    learnData, testData, i, LEARN_RATE, use)
                print("Using test data for testing") if use else print(
                    "Using learn data for testing")
                print("Activation function: ", end='')
                print("step") if i == 0 else print("sigmoid")
                print(f"Positives: {positives[-1]}")
                print(f"Cost: {cost[-1]}")
                print(f"Weights: {w}")
                plot(positives, "Accuracy (%)")
                plot(cost, "Error")
                print()


if __name__ == "__main__":
    main()
