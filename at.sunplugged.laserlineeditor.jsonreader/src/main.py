'''
Created on 24.04.2017

@author: jasch
'''

import argumentParser
import sys
from svgReader import createLaserScriptFromSvg
from Tkinter import Tk
from Gui import App


if __name__ == '__main__':
    arguments = []
    if (len(sys.argv) > 1):
        arguments = argumentParser.parseArguments(sys.argv)
        fileName = arguments[0]
        nullX = arguments[1]
        nullY = arguments[2]
        script = createLaserScriptFromSvg(fileName, nullX, nullY)
        print script
        outputFile = open(fileName.replace(".svg", ".txt"), 'w')
        outputFile.write(script)
        outputFile.close()
    else:
        root = Tk()
        app = App(root)
        root.mainloop()
    
    
