'''
Created on 24.04.2017

@author: jasch
'''

import argumentParser
import sys
from svgReader import createLaserScriptFromSvg


if __name__ == '__main__':
    arguments = []
    if (len(sys.argv) > 1):
        arguments = argumentParser.parseArguments(sys.argv)
    else:
        arguments.append(raw_input("Enter filename:\n"))
        arguments.append(raw_input("Enter nullX:\n"))
        arguments.append(raw_input("Enter nullY:\n"))
    
    fileName = arguments[0]
    nullX = arguments[1]
    nullY = arguments[2]
    script = createLaserScriptFromSvg(fileName, nullX, nullY)
    print script
    outputFile = open(fileName.replace(".svg", ".txt"), 'w')
    outputFile.write(script)
    outputFile.close()
