'''
Created on 09.05.2017

@author: jasch
'''


import xml.etree.ElementTree as ET
from types import NoneType
import re
from operator import add
import jsonIds
from jsonIds import LaserLine
import laserLineAlgorithm
from laserLineAlgorithm import createLaserScriptFromLaserLines,\
    createScriptFromLaserLinesWithExplicitNullPoint



"""
for child in root:
    print child.tag, child.attrib
    

for group in root.findall('{http://www.w3.org/2000/svg}g'):
    groupmode = group.get('{http://www.inkscape.org/namespaces/inkscape}groupmode')
    label = group.get('{http://www.inkscape.org/namespaces/inkscape}label')
    print groupmode, label
            
"""
def findAllLayers(root):
    layers = []
    for group in root.findall('{http://www.w3.org/2000/svg}g'):
        groupmode = groupmode = group.get('{http://www.inkscape.org/namespaces/inkscape}groupmode')
        if groupmode == 'layer':
            layers.append(group)
    return layers



def findRootXandY(root):
    x = 0
    y = str(root.get('height'))
    y = y.replace('mm', '')
    return [x, int(y)]    

def checkIfLaserElement(element):
    titleTag = element.find('{http://www.w3.org/2000/svg}title')
    if type(titleTag) == NoneType:
        return False
    title = titleTag.text
    if type(title) != NoneType and title.lower() == 'laser':
        return True
    else:
        return False
    

transformRegex = re.compile('([\d\.-]+)')

def getTranslateValues(element):
    transform = element.get('transform')
    if type(transform) != NoneType:
        transform = transform.replace("translate(", "")
        transform = transform.replace(")", "")
        xandy = transform.split(",")
        return [float(xandy[0]), -float(xandy[1])]
    else:
        return [0, 0]


def getLaserSettings(child):
    description = child.find('{http://www.w3.org/2000/svg}desc')
    if type(description) is NoneType:
        return NoneType
    
    text = description.text
    keyAndParameters = text.split(";")
    speed = -1
    power = -1
    freq = -1
    
    for keyAndParameter in keyAndParameters:
        key = keyAndParameter.split(":")[0]
        value = keyAndParameter.split(":")[1]
        if key.lower() == "speed":
            speed = int(value)
        elif key.lower() == "power":
            power = int(value)
        elif key.lower() == "freq":
            freq = int(value)
    
    if speed != -1 and power != -1 and freq != -1:
        return [power, freq, speed]
    return NoneType
    
    

def findLaserElements(topChild, currentPosition, laserSettings):
    laserLines = []
    for child in topChild:
        childPosition = map(add, currentPosition, getTranslateValues(child))
        
        currentLaserSettings = getLaserSettings(child)
        if currentLaserSettings is NoneType:
            currentLaserSettings = laserSettings
        if checkIfLaserElement(child) == True:
            handleLaserElement(child, childPosition, currentLaserSettings, laserLines)
        else:
            laserLines.append(findLaserElements(child, childPosition, currentLaserSettings))
    
    return laserLines
        
def handleLaserElement(child, currentPosition, laserSettings, laserLines):
    
   
    currentLaserSettings = getLaserSettings(child)
    if currentLaserSettings is NoneType:
        currentLaserSettings = laserSettings
    if child.tag == "{http://www.w3.org/2000/svg}g":
       
        for subchild in child:
            subCurrentLaserSettings = getLaserSettings(subchild)
            if subCurrentLaserSettings is NoneType:
                subCurrentLaserSettings = currentLaserSettings
                
            handleLaserElement(subchild, map(add, currentPosition, getTranslateValues(subchild)), subCurrentLaserSettings, laserLines)
    elif child.tag == "{http://www.w3.org/2000/svg}rect":
        x = float(child.get('x'))
        y = float(child.get('y'))
        width = float(child.get('width'))
        height = float(child.get('height'))
        laserLines.append(LaserLine(xStart=int(round(currentPosition[0] + x, 3) * 1000), xEnd=int(round(currentPosition[0] + x + width, 3)  * 1000), yStart=int(round(currentPosition[1] - y - height, 3) * 1000), yEnd=int(round(currentPosition[1] - y - height, 3) * 1000), power=currentLaserSettings[0], frequency=currentLaserSettings[1], speed=currentLaserSettings[2]))
        
        
    
def createLaserScriptFromSvg( fileName, nullX = 0, nullY = 0 ):
    
    tree = ET.parse(fileName)

    root = tree.getroot()
    
    laserLines = []
    for layer in findAllLayers(root):
        currentPosition = findRootXandY(root)
        currentPosition = map(add, currentPosition, getTranslateValues(layer))
        laserSettings = getLaserSettings(layer)
        newLines = findLaserElements(layer, currentPosition, laserSettings)
        for line in newLines:
            laserLines.append(line)
    
    return createScriptFromLaserLinesWithExplicitNullPoint(laserLines, nullX, nullY)

