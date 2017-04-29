'''
Created on 24.04.2017

@author: jasch
'''

import json
import jsonIds

def decodeFile( fileHandle ):
    jsonObject = json.load(fileHandle)
    dictinary = {}
    dictinary[jsonIds.NULL_ID] = extractNullPoint(jsonObject)
    dictinary[jsonIds.LASER_LINE_ID] = extractLaserLines(jsonObject)
    return dictinary
    
    
    
def extractNullPoint( jsonObject ):
    if jsonIds.NULL_ID in jsonObject:
        item = jsonObject[jsonIds.NULL_ID]
        return jsonIds.NullPoint(item['x'], item['y'])
    else:
        raise ValueError('No Null-point found in json file')

def extractLaserLines( jsonObject ):
    if jsonIds.NULL_ID in jsonObject:
        item = jsonObject[jsonIds.LASER_LINE_ID]
        returnList = []
        for line in item:
            returnList.append(jsonIds.LaserLine(line['xStart'], line['xEnd'], line['yStart'], line['yEnd'], line['speed'], line['power'], line['frequency']))
        return returnList