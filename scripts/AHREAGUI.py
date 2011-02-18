#! /usr/bin/env python
import Tkinter

from GUI.AHREAApp import AHREAApp
from GUI.AHREAController import AHREAController
import os.path
root = Tkinter.Tk()
root.minsize(width=350, height=300)
cont = AHREAController(os.path.join('data','config.xml'))
app = AHREAApp(root, cont)
cont.setApp(app)
root.mainloop()
