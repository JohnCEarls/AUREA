#! /usr/bin/env python
import Tkinter
from AUREA.GUI.App import App
from AUREA.GUI.Controller import Controller
import os
import tkFileDialog
from tkMessageBox import *

# if you are running this somewhere other than the workspace folder
# set workspace to the path of the directory that contains data/config.xml

workspace = os.getcwd()

root = Tkinter.Tk()
cont = Controller(workspace=workspace)
app = App(root, cont)
cont.setApp(app)
root.mainloop()

