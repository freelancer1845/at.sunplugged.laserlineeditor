'''
Created on 29.04.2017

@author: jasch
'''

import jsonIds
import math
from operator import attrgetter


def intialCommands():
    return '6;LACT\n3;ALLIGN;1500;-0.215\n'


def startingPoint(dictionary):
    startingPointText = []
    startingPointText.append('*-----Starting Point-----*\n')
    nullPointItem = dictionary[jsonIds.NULL_ID]
    startingPointText.append('0;NULL;' + str(nullPointItem.x) + ';' + str(nullPointItem.y) + '\n')
    return ''.join(startingPointText)
    

def groupLaserLinesByPower(sortedLaserLines):
    iterator = iter(sortedLaserLines)
    currentPower = 0
    currentFrequency = 0
    groupList = []
    try:
        currentLine = iterator.next()
        currentPower = currentLine.power
        currentFrequency = currentLine.frequency
        group = [currentLine]
        while(True):
            try:
                currentLine = iterator.next()
                if currentLine.power == currentPower and currentLine.frequency == currentFrequency:
                    group.append(currentLine)
                else:
                    groupList.append(group)
                    group = [currentLine]
                    currentPower = currentLine.power
                    currentFrequency = currentLine.frequency
            except StopIteration:
                if len(group) > 0:
                    groupList.append(group)
                break
    except StopIteration:
        raise ValueError('No laser line to sort...')
    
    return groupList
                        
    

def createPowerHeader(group):
    laserLine = group[0]
    return '*-----Setting new power-----Power:' + str(laserLine.power) + '---Frequency:' + str(laserLine.frequency) + '-----\n6;LPAR;' + str(laserLine.power) + ';' + str(laserLine.frequency) + '\n'


def createLaseringScript(group):
    script = []
    sortedByYStart = sorted(group, key=attrgetter('yStart'))
    previousX = 0
    for line in sortedByYStart:
        distanceXStart = abs(line.xStart - previousX)
        distanceXEnd = abs(line.xEnd - previousX)
        if (distanceXEnd < distanceXStart):
            script.append('0;LASERNXY;{},{},{},{},{}\n'.format(str(line.xEnd), str(line.yStart), str(line.xStart), str(line.yEnd), str(line.speed)))
            previousX = line.xStart
        else:
            script.append('0;LASERNXY;{},{},{},{},{}\n'.format(str(line.xStart), str(line.yStart), str(line.xEnd), str(line.yEnd), str(line.speed)))
            previousX = line.xEnd
    
    return ''.join(script)


def createFinish():
    script = []
    script.append('*----- Finish -----\n')
    script.append('*---Coming Home---\n')
    script.append('0;PAY;100000;100000\n')
    script.append('0;ERR\n')
    return ''.join(script)
    


def createScriptForLaserLineGroup(group):
    script = []
    script.append(createPowerHeader(group))
    script.append(createLaseringScript(group))
    script.append(createFinish())
    
    return "".join(script)

def createLaserScript(dictionary):
    script = []
    laserLines = dictionary[jsonIds.LASER_LINE_ID]
    laserLines = sorted(laserLines, key=attrgetter('power', 'frequency'), reverse=True)
    groupedLines = groupLaserLinesByPower(laserLines)
    for group in groupedLines:
        script.append(createScriptForLaserLineGroup(group))
    return ''.join(script)


def createScriptFromJsonDictionary(dictionary):
    script = []
    
    '''Creates the header of the script'''
    script.append('*---------------Python created script for lasering sunplugged.at. Created by Jascha Riedel---------*\n')
    script.append(intialCommands())
    
    ''' Create starting point (null point)'''
    script.append(startingPoint(dictionary))
    
    ''' Create the laser lines. This is the actual complex alogirthm'''
    script.append(createLaserScript(dictionary))
    
    
    return "".join(script)
    
    
    
    
    
    
