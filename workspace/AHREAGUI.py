#! /usr/bin/env python
import Tkinter
from AHREA.GUI.AHREAApp import AHREAApp
from AHREA.GUI.AHREAController import AHREAController
import os.path
import tkFileDialog
from tkMessageBox import *

# if you are running this somewhere other than the workspace folder
# set workspace to the path of the directory that contains data/config.xml

workspace = os.getcwd()

root = Tkinter.Tk()
root.minsize(width=350, height=300)
cont = AHREAController(workspace=workspace)
app = AHREAApp(root, cont)
cont.setApp(app)
root.mainloop()

