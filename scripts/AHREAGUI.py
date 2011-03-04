#! /usr/bin/env python
import Tkinter
from AHREA.GUI.AHREAApp import AHREAApp
from AHREA.GUI.AHREAController import AHREAController
import os.path
import tkFileDialog
from tkMessageBox import *

root = Tkinter.Tk()
root.minsize(width=350, height=300)
cont = AHREAController()
app = AHREAApp(root, cont)
cont.setApp(app)
root.mainloop()

