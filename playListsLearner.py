'''
Created on 2013-4-19

@author: YixinGeng
'''
import json
import bpnn
import sys
import math
import random

def makePlayLists():
    playList = []
    for i in range(3):
        if random.random() > 0.5:
            playList.append(1)
        else:
            playList.append(0)
    return playList

def saveTrainData():
    fileName = "songs.json"
    f = open(fileName, 'r')
    data = json.loads(f.read())
    trainData = []
    for i in range(100):
        song = data[i]
        listNum = makePlayLists()
        song.setdefault('lists', listNum)
        trainData.append(song)
    print trainData
    f = open('trainset.json', 'w')
    f.write(json.dumps(trainData))        

def saveTestData():
    fileName = "songs.json"
    f = open(fileName, 'r')
    data = json.loads(f.read())
    trainData = []
    for i in range(500, 600):
        song = data[i]
        trainData.append(song)
    print trainData
    f = open('testset.json', 'w')
    f.write(json.dumps(trainData))

def normalizeInputData(inputData):
    sqSum = 0
    vectorLen = 0
    normalizedInputData = []
    for attribute in inputData:
        sqSum += math.pow(attribute, 2.0)
    vectorLen = math.sqrt(sqSum)
    for attribute in inputData:
        normalizedInputData.append(attribute / vectorLen)
    return normalizedInputData

def makeInputData(song):
    inputData = []
    inputData.append(int(song['time_signature']))
    inputData.append(song['energy'])
    if song['energy'] != 0:
        print song
    inputData.append(song['tempo'])
    inputData.append(song['danceability'])
    if song['danceability'] != 0:
        print song
    inputData.append(int(song['key']))
    inputData.append(song['duration'])
    inputData.append(song['loudness'])
    inputData = normalizeInputData(inputData)

    return inputData

def makeTrainingDataSet():
    fileName = 'trainset.json'
    f = open(fileName, 'r')
    data = json.loads(f.read())
    trainDataSet = []
    for song in data:
        inputData = makeInputData(song)
        outputData = song['lists']
        trainDataSet.append([inputData, outputData])
    return trainDataSet
    
def makeTestDataSet():
    fileName = 'testset.json'
    f = open(fileName, 'r')
    data = json.loads(f.read())
    testDataSet = []
    for song in data:
        inputData = makeInputData(song)
        testDataSet.append([inputData, []])
    return testDataSet, data  

# def playListClassifier(network):

    
    
    
def songClassifier():
    trainDataSet = makeTrainingDataSet()
    network = bpnn.NN(7, 10, 3)
    network.train(trainDataSet)
    unSortedDataSet, data = makeTestDataSet()
    fileName = 'sortedset.json'
    f = open(fileName, 'w')
    result = network.test(unSortedDataSet)
    sortedResult = []
    for i in range(len(unSortedDataSet)):
        sortedSong = {}
        sortedSong.setdefault('title', data[i]['title'])
        sortedSong.setdefault('artist', data[i]['artist'])
        sortedSong.setdefault('lists', result[i]) 
        sortedResult.append(sortedSong)
    print sortedResult
    f.write(json.dumps(sortedResult))        
#     print unSortedDataSet[0]
#     print data[0]
    
# def main():
#     print json.loads(f.read())
#     # Teach network XOR function
#     pat = [
#         [[0,0], [0, 1]],
#         [[0,1], [1, 2]],
#         [[1,0], [1, 2]],
#         [[1,1], [0, 2]]
#     ]
# 
#     # create a network with two input, two hidden, and one output nodes
#     n = bpnn.NN(2, 2, 2)
#     # train it with some patterns
#     n.train(pat)
#     n.weights()
#     # test it
#     n.test(pat)
    
    
    
if __name__ == '__main__':
#     saveTrainData()
    songClassifier()