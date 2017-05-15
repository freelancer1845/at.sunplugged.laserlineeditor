'''
Created on 15.05.2017

@author: jasch
'''


from Tkinter import *
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfile
from svgReader import createLaserScriptFromSvg


class App:
    def __init__(self, master):
        master.geometry("400x220")
        master.title("SVG Laser Script creator")
        
        self.loadButton = Button(master, text = 'Load Button', command=self.loadFile)
        self.loadButton.grid(row=1, column=1, pady=(10, 50))
        self.currentFileEntry = Entry(master, text= "...")
        self.currentFileEntry.grid(row=1, column=2, sticky=E, pady=(10, 50))

        self.nullXLabel = Label(master, text="NullX:")
        self.nullXLabel.grid(row=2, column=1)
        self.nullXEntry = Entry(master)
        self.nullXEntry.grid(row=2, column=2)
        
        self.nullYLabel = Label(master, text="NullY:")
        self.nullYLabel.grid(row=3, column=1)
        self.nullYEntry = Entry(master)
        self.nullYEntry.grid(row=3, column=2)
        
        self.createButton = Button(master, text = 'Create and save Script', command=self.createAndSaveScript)
        self.createButton.grid(row=4, column=1, pady= (50, 10))
        
    def loadFile(self):
        name = askopenfilename()
        self.currentFileEntry.delete(0, END)
        self.currentFileEntry.insert(0, name)
        
    def createAndSaveScript(self):
        fileHandle = asksaveasfile('w')
        script = createLaserScriptFromSvg(self.currentFileEntry.get(), self.nullXEntry.get(), self.nullYEntry.get())
        fileHandle.write(script)
        fileHandle.close()
    

