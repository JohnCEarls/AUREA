#! /usr/bin/env python
import Tkinter
from AUREA.GUI.AUREAApp import AUREAApp
from AUREA.GUI.AUREAController import AUREAController
import os
import tkFileDialog
from tkMessageBox import *

# if you are running this somewhere other than the workspace folder
# set workspace to the path of the directory that contains data/config.xml

workspace = os.getcwd()

root = Tkinter.Tk()
cont = AUREAController(workspace=workspace)
app = AUREAApp(root, cont)
cont.setApp(app)
root.mainloop()

