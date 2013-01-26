#! /usr/bin/env python
import Tkinter
from AUREA.GUI.App import App
from AUREA.GUI.Controller import Controller
import os
import tkFileDialog
from tkMessageBox import *
import re
import platform

import imp, os, sys

def main_is_frozen():
   return (hasattr(sys, "frozen") or # new py2exe
           hasattr(sys, "importers") # old py2exe
           or imp.is_frozen("__main__")) # tools/freeze

def get_main_dir():
   if main_is_frozen():
       return os.path.dirname(sys.executable)
   return os.path.dirname(sys.argv[0])

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

if platform.system() == 'Windows' and main_is_frozen():
    #py2exe standalone
    appdata = os.getenv('APPDATA')
    if appdata is not None:
        workspace = os.path.join(appdata, 'AUREA')
        
        if not os.path.exists(workspace):
            os.mkdir(workspace)
        if not os.path.exists(os.path.join(workspace, 'data')):
            os.mkdir(os.path.join(workspace, 'data'))
        #copy files
        needful_things = ['config.xml', 'AUREA-logo-200.pgm', 'Homo_sapiens.gene_info.gz','c2.biocarta.v2.5.symbols.gmt' ]
        for thing in needful_things:
            if not os.path.exists( os.path.join(workspace, 'data', thing)):
                shutil.copy(os.path.join(old_workspace, 'data',thing), os.path.join(workspace, 'data'))
        os.chdir(workspace)


elif platform.system() == 'Darwin' and re.compile(r'AUREA\.app').search(init_workspace):
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
    if not os.path.exists(os.path.join(workspace, 'data')):
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

