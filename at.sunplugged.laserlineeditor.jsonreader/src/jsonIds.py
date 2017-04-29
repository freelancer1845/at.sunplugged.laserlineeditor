'''
Created on 24.04.2017

@author: jasch
'''


NULL_ID = 'NULL-POINT'

class NullPoint:
    ''' Represents a NULL-POINT command'''
    x = 0
    y = 0
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
LASER_LINE_ID = "LASERLINE"

class LaserLine:
    ''' Represents a basic Lasered Line'''
    xStart = 0
    xEnd = 0
    yStart = 0
    yEnd = 0
    speed = 0
    power = 0
    frequency = 0
    
    def __init__(self, xStart, xEnd, yStart, yEnd, speed, power, frequency):
        self.xStart = xStart
        self.xEnd = xEnd
        self.yStart = yStart
        self.yEnd = yEnd
        self.speed = speed
        self.power = power
        self.frequency = frequency
        
