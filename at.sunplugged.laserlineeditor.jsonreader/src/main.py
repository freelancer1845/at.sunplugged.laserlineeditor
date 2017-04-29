'''
Created on 24.04.2017

@author: jasch
'''

import fileDecoder
import laserLineAlgorithm


if __name__ == '__main__':
  
    fileHandle = open('jsonTest.txt', 'r')
    print(laserLineAlgorithm.createScriptFromJsonDictionary(fileDecoder.decodeFile(fileHandle)))
    
    
