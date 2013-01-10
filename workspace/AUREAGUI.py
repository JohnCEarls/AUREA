#! /usr/bin/env python
import Tkinter
from AUREA.GUI.App import App
from AUREA.GUI.Controller import Controller
import os
import tkFileDialog
from tkMessageBox import *
import re

def newWorkspace(root):
    """
    Lets user choose a new workspace location 
    """
    import tkFileDialog 
    options = {}
    options['parent']= root 
    options['title'] = 'Choose Workspace Location'
    workspace_dir = tkFileDialog.askdirectory(**options)
    return workspace_dir




# if you are running this somewhere other than the workspace folder
# set workspace to the path of the directory that contains data/config.xml

root = Tkinter.Tk()
init_workspace =  os.getcwd()

if re.compile('Application').search(init_workspace):
    #this is a py2app build
    #move workspace out of the application folder
    import shutil
    old_workspace = init_workspace
    new_ws_location = newWorkspace(root)
    
    workspace = os.path.join(new_ws_location, 'workspace')
    #create workspace folder
    if not os.path.exists(workspace):
        os.mkdir(workspace)
    #create data folder
    if not os.path.exists(workspace, 'data'):
        os.mkdir(os.path.join(workspace, 'data'))
    #copy files
    needful_things = ['config.xml', 'AUREA-logo-200.pgm', 'Homo_sapiens.gene_info.gz','c2.biocarta.v2.5.symbols.gmt' ]
    for thing in needful_things:
        if not os.path.exists( os.path.join(workspace, 'data', thing)):
            shutil.copy(os.path.join(old_workspace, 'data',thing), os.path.join(workspace, 'data'))
    os.chdir(workspace)
else:
    workspace = init_workspace
    
cont = Controller(workspace=workspace)
app = App(root, cont)
cont.setApp(app)
root.mainloop()

