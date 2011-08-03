from Tkinter import *
import tkFileDialog
import tkMessageBox
import os
from AUREA.GUI.Results import *
import platform
import Queue
import re
import threading

def run_in_thread(fn):
    """
    A decorator that causes a function to be run in a thread
    see:http://amix.dk/blog/post/19346
    """
    def run(*k, **kw):
        self = k[0]

        self.disableButtons()
        #Buttons reenabled in App.App.checkTMQ(), by 'releaseButtons' message
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
    return run

def thread_error_catch(fn):
    """
    A decorator to catch errors in a thread and pass them back to the
    mainloop.
    """
    def run(*k, **kw):        
        self = k[0]
        try:
            fn(*k, **kw)
            self.thread_message_queue.put(('releaseButtons',None))
        except Exception, e:
            self.thread_message_queue.put(('error', sys.exc_info()))
    return run

   

class Page(Frame):
    """
    Base class for data input frames
    """
    def __init__(self, root, id):
        Frame.__init__(self, root)
        self.config(relief=GROOVE,padx=5, borderwidth=2)
        self.root = root
        self.remote = root.remote
        self.id = id
        self.thread_message_queue = self.root.thread_message_queue     



    def drawPage(self):
        """
        Called when page is brought up for display
        """

        raise ImplementationError(self.id, 'drawPage')

    def setUpPage(self):
        """
        Called when page is brought up for display
        """

        raise ImplementationError(self.id, 'setUpPage')

    def clearPage(self):
        raise ImplementationError(self.id, 'clearPage')
    
    def _boldFont(self, w):
        import tkFont
        font = tkFont.Font(font=w['font'])
        font.config(weight='bold')
        w['font'] = font

    def _italicFont(self, w):
        import tkFont
        font = tkFont.Font(font=w['font'])
        font.config(slant=tkFont.ITALIC)
        w['font'] = font



    def setAppTitle(self, title):
        self.root.setAppTitle(title)

    def clearGrid(self):
        for widget in self.grid_slaves():
            widget.grid_forget()
    
    def adaptiveGood(self):
        """
        checks that the target accuracy and max running time are set.
        Used in train and evaluate
        """
        acc =  self.auto_target_acc.get()
        mt = self.auto_maxtime.get()
        errmsg = ""
        if len(acc.strip()) == 0:
            errmsg += "Adaptive requires a target accuracy."
        if len(mt.strip()) == 0:
            errmsg += "Adaptive requires a maximum running time."

        if len(errmsg) > 0:
            self.thread_message_queue.put(('adaptiveMessage', errmsg)) 
            return False
        else:
            return True

    def disableButtons(self):
        """
        Stub-used when we are doing something that we need to keep
        the user from interfering with.
        Each page that needs this is responsible for overriding this
        """
        pass

    def enableButtons(self):
        """
        Stub- okay for user to interact with GUI
        """
        pass

class HomePage(Page):
    """
    Corresponds to the Data Summary/Home page
    """
    
    def __init__(self, root):
        Page.__init__(self, root, 'Home')
        

    def setUpPage(self):
        pass
 
    def setupDataFileFrame(self):
        dff = self.dataFileFrame = Frame(self)
        c = self.root.controller
        if len(c.softFile) > 0:
            for i,sf in enumerate(c.softFile):
                _, fname = os.path.split(sf)
                l = Label(dff, text="Data File:")
                self._boldFont(l)
                l.grid(row=i, column=0, sticky=E)
                fl = Label(dff, text=fname)
                fl.grid(row=i, column=1, sticky=W)
            ngenes, nprobes =c.getDataPackagingResults()
            l = Label(dff, text="Num. genes:")
            r = len(c.softFile)
            l.grid(row=r, column=0, sticky=E)
            fl = Label(dff, text=ngenes)
            fl.grid(row=r, column=1, sticky=W)
            l = Label(dff, text="Num. probes:")
            r += 1
            l.grid(row=r, column=0, sticky=E)
            fl = Label(dff, text=nprobes)
            fl.grid(row=r, column=1, sticky=W)
        else:
            l = Label(dff, text="Data File:")
            self._boldFont(l)
            l.grid(row=0, column=0, sticky=E)
            nf = Label(dff, text="Not specified", fg="red")
            nf.grid(row=0, column=1, sticky=W)
            
       
    def setupGeneNetworkFileFrame(self):
        gnff = self.geneNetworkFileFrame = Frame(self)
        c = self.root.controller
        ni = c.getNetworkInfo()
        tfl = Label(gnff, text ="Gene Network File:" )
        self._boldFont(tfl)
        tnets = Label(gnff, text = "Num. networks:")
        tgenes = Label(gnff, text="Network size:")
        if ni is not None:
            fl = Label(gnff, text = os.path.split(ni[0])[1])
            nets = Label(gnff, text = ni[1])
            genestr = str(ni[4])+  '-' + str(ni[3]) + '(ave. ~' + str(int(ni[2])) +')'
            genes = Label(gnff, text=genestr)
        else:
            fl = Label(gnff, text ="Not specified", fg="red" )
            nets = Label(gnff, text ="" )
            genes = Label(gnff, text="")
        tfl.grid(row=0,column=0, sticky=E) 
        tnets.grid(row=1,column=0, sticky=E) 
        tgenes.grid(row=2,column=0, sticky=E) 
        fl.grid(row=0,column=1, sticky=W) 
        nets.grid(row=1,column=1, sticky=W) 
        genes.grid(row=2,column=1, sticky=W) 
       
    def setupClassFrame(self):
        """
        Builds the classes frame
        """
        cf = self.classFrame = Frame(self)
        c = self.root.controller
        ci =c.getClassificationInfo()
        tfl = Label(cf, text ="Classes:" )
        self._boldFont(tfl)
        tc1 = Label(cf, text = "Class 1 (size):")
        tc2 = Label(cf, text="Class 2 (size):")
        c1 = ci[0] + " (" + str(ci[1])+")"
        c2 = ci[2] + " (" + str(ci[3])+")"
           
        lc1 = Label(cf, text=c1)
        lc2 = Label(cf, text=c2)
        if ci[1] == 0:
            ns = Label(cf, text ="Not specified", fg="red" )
            ns.grid(column=1, row=0, sticky=W)
        tfl.grid(row=0,column=0, sticky=E) 
        tc1.grid(row=1,column=0, sticky=E) 
        tc2.grid(row=2,column=0, sticky=E) 
        lc1.grid(row=1,column=1, sticky=W) 
        lc2.grid(row=2,column=1, sticky=W) 
        cf.columnconfigure( 0, weight = 1 )
        cf.columnconfigure( 1, weight = 1 )
    def showResults(self, learner):
        if learner=='tsp':
            TSPResults(self)
        elif learner == 'ktsp':
            KTSPResults(self)
        elif learner == 'tst':
            TSTResults(self)
        elif learner ==  'dirac':
            DiracResults(self)
        elif learner ==  'ada':
            AdaptiveResults(self)


    def setupLearningAlgorithmFrame(self):

        c = self.root.controller
        lf = self.learningAlgorithmFrame = Frame(self)
        bc = Label(lf, text="Best Classifiers(T1,F1,T2,F2,MCC):")
        cp = Label(lf, text="CV Performance(MCC):")
        self._boldFont(cp)
        self._boldFont(bc)

        tp = Label(lf, text="TSP:")
        kp = Label(lf, text="k-TSP:")
        tt = Label(lf, text="TST:")
        di = Label(lf, text="DiRaC:")
        ad = Label(lf, text="Adaptive:")
        lList = [tp, kp, tt, di, ad]

        nt = Label(lf, text="Not trained", fg="red")
        nc = Label(lf, text="Not calculated", fg="red")
        bd = {}
        acc = c.getLearnerAccuracy()
        cv = c.getCrossValidationResults()
        for i,l in enumerate(['tsp','ktsp','tst', 'dirac', 'ada']):
            lList[i].grid(row=i+1, column=0, sticky=E)
            myalg = l
            #so dumb, for some reason cannot pass l or myalg(ref or some such nonsense)
            if l=='tsp':
                bd[l]  = Button(lf, text="More info...", command=lambda: self.showResults('tsp'))
              
            elif l == 'ktsp':
                 bd[l]  = Button(lf, text="More info...", command=lambda: self.showResults('ktsp'))
            elif l == 'tst':
                  bd[l]  = Button(lf, text="More info...", command=lambda: self.showResults('tst'))
            elif l ==  'dirac':
                bd[l]  = Button(lf, text="More info...", command=lambda: self.showResults('dirac'))
            elif l ==  'ada':
                bd[l]  = Button(lf, text="More info...", command=lambda: self.showResults('ada'))

         
            #bd[l]  = Button(lf, text="More info..." + l, command=lambda: self.showResults(myalg))
            bd[l].grid(row=i+1, column=2,sticky=E+W, padx=5)
            nt = Label(lf, text="Not trained", fg="red")
            nc = Label(lf, text="Not calculated", fg="red")
            #handle apparent accuracy
            if acc[i] is None:
                bd[l].configure(state=DISABLED)
                nt.grid(row=i+1, column=1,sticky=W)
            else:
                toStr = ','.join([str(x)[:4] for x in acc[i]])
                lab = Label(lf, text=toStr, padx=5 )
                lab.grid(row=i+1, column=1,sticky=W)
            #handle cross validation
            if cv[i] is None:
                nc.grid(row=i+1, column=3)
            else:
                lab = Label(lf, text=str(cv[i])[:4])
                lab.grid(row=i+1, column=3)
        bc.grid(row=0, column=0,columnspan=3, sticky=W)
        cp.grid(row=0, column=3)
        lf.rowconfigure( 0, weight = 1 )
        lf.columnconfigure( 2, weight = 1 )

       
        


    def drawPage(self):       
        
        self.setAppTitle("Data Summary") 
        self.setupDataFileFrame()
        self.setupGeneNetworkFileFrame()       
        self.dataFileFrame.grid(column=0, row=0, sticky=N+W,padx=5)
        self.geneNetworkFileFrame.grid(column=1, row=0, sticky=N+E,padx=5) 
        self.setupClassFrame()
        self.classFrame.grid(column=0, columnspan=2, row=1,  sticky=E+W, pady=10)
        self.setupLearningAlgorithmFrame()
        self.learningAlgorithmFrame.grid(column=0, columnspan=3, row=2, sticky=S+E+W)
    def clearPage(self):
        self.clearGrid()
        self.grid_forget()

class ImportDataPage(Page):
    """
    Page to choose data files
    """
    def __init__(self, root):
        Page.__init__(self, root, 'Import')
        self.gnPath = None
        self.softFilePath = None
        self.gsynPath = None
        #init softfile lists
        self.softFileLabel = []
        self.softFilePath = []
        self.softFilePathE = []
        self.softFileDialogButton = []
        self.softFileDeleteButton = []
        self.dataSettingButton=None
        self.addButton = None    
        self.buttonList = []
        

    def drawPage(self):
        self.setAppTitle("Import Data")
        ypad = 3
        r = 1
        
        for i in range( len(self.softFileLabel) ):
            self.softFileLabel[i].grid(row=r, column=0, pady=ypad)
            self.softFilePathE[i].grid(row=r, column=1, pady=ypad)
            self.softFileDialogButton[i].grid(row=r, column=2, pady=ypad)
            
            if len(self.softFileLabel) != 1:
                self.softFileDeleteButton[i].grid(row=r, column=3, pady=ypad)
            r += 1
        #one off buttons
        self.addButton.grid(row=r, column=2, pady=ypad, sticky=N)
        self.downloadButton.grid(row=r, column=1, pady=ypad, sticky=E+N)
        self.dataSettingsButton.grid(row=r, column=0, pady=ypad, sticky=W+N)
        r += 1

        self.gnLabel.grid(row=r, column=0, pady=ypad)
        self.gnPathE.grid(row=r, column=1, pady=ypad)
        self.gnDialogButton.grid(row=r, column = 2, pady=ypad)
        r += 1
        self.gnText.grid(row=r, column=0, pady=ypad, columnspan=2, sticky=E+W)
        r+=1
        
        self.gsynLabel.grid(row=r, column=0, pady=ypad)
        self.gsynPathE.grid(row=r, column=1, pady=ypad)
        self.gsynDialogButton.grid(row=r, column = 2, pady=ypad)
        r+=1
        self.gsynText.grid(row=r, column=0, pady=ypad, columnspan=2, sticky=E+W)
        numcolumns, numrows = self.grid_size()
        self.import_button.grid(row=numrows, column=numcolumns-2,columnspan=2, padx=10, sticky=E+W)
        self.grid(row=1,column=1, sticky=N+S+E+W)
        numcolumns, numrows = self.grid_size()
        #self.rowconfigure(numrows-1 , weight = 0 )
        self.rowconfigure(numrows-1 , weight = 1 )
        self.columnconfigure( 1, weight = 1 )
        
    def setUpPage(self):
        self.buttonList = []
        self.softFileDisplay()
        self.geneNetworkDisplay()
        #there can be only 1
        if self.addButton is None:
            a=self.addButton = Button(self, text="Add another file",command=self.softfileadd)
            b=self.downloadButton = Button(self, text="Download...", command=self.downloadSOFTdialog)
            c=self.dataSettingsButton = Button(self, text="Data Settings", command=self.root.menu.data_settings)
            self.buttonList.append(a)
            self.buttonList.append(b)
            self.buttonList.append(c)
            
        
        self.geneSynonymDisplay()    
        self.import_button = Button(self, text="Import Files", command=self.importFiles)
        if len(self.softFilePath) > 0 and len(self.softFilePath[0].get().strip()) == 0:#only disable if there are no files
            self.import_button.config(state=DISABLED)

    def clearGrid(self):
        for widget in self.grid_slaves():
            widget.grid_forget()
        
    def clearPage(self):
        self.clearGrid()
        self.grid_forget()

    def softFileDisplay(self, add=False):
        if len(self.softFilePath) == 0 or add:
            index = len(self.softFileLabel)
            self.softFileLabel.append(Label(self, text="Data File : "))

            sv = StringVar()
            self.softFilePath.append(sv)
            
            self.softFilePathE.append(Entry(self, textvariable=self.softFilePath[-1],width=50))
            self.softFileDialogButton.append(Button(self, text = "Browse ...",command=lambda: self.softfiledialog(sv)))
            self.softFileDeleteButton.append(Button(self, text = "Remove", command = lambda:    self.softfiledelete(index)))
    
    def softfiledelete(self, index):
        self.clearPage()
        del self.softFileLabel[index]
        del self.softFilePath[index]
        del self.softFilePathE[index]
        del self.softFileDialogButton[index]
        del self.softFileDeleteButton[index]
        #reset delete indices
        for i in range(len(self.softFileLabel)):
            self.softFileDeleteButton[i].configure(command = lambda: self.softfiledelete(i))
        self.drawPage()
        self.import_button.config(state=NORMAL)

    def softfileadd(self):
        self.softFileDisplay(add=True)
        self.clearPage()
        self.drawPage()
        
    def geneNetworkDisplay(self):
        self.gnLabel = Label(self, text="Gene Network File : ")
        if self.gnPath is None:
            self.gnPath = StringVar()
        self.gnPathE = Entry(self, textvariable=self.gnPath,width=50)
        a = self.gnDialogButton = Button(self, text = "Browse ...",command=self.gnfiledialog)
        self.buttonList.append(a)
        self.gnText = Label(self, text="Required for DiRaC, Adaptive (c2.biocarta.v2.5.symbols.gmt)")
        self._italicFont(self.gnText)

    def geneSynonymDisplay(self):
        self.gsynLabel = Label(self, text="Gene Synonym File : ")
        if self.gsynPath is None:
            self.gsynPath = StringVar()
        self.gsynPathE = Entry(self, textvariable=self.gsynPath, width=50)
        a=self.gsynDialogButton = Button(self, text = "Browse ...",command=self.gsynfiledialog) 
        self.buttonList.append(a)
        self.gsynText = Label(self, text="Recommended for DiRaC, Adaptive (Homo_sapiens.gene_info.gz)")
        self._italicFont(self.gsynText)



    def softfiledialog(self, pathVariable):
        file_opt = options =  {}
        if platform.platform()[0:3] != 'Dar':#mac no like 
            options['filetypes'] = [('gzipped SOFT', '.soft.gz'), ('SOFT', '.soft'),('Comma Separated', '.csv')]
        options['parent'] = self
        options['initialdir'] = 'data'

        options['title'] = "AUREA - Select data file."
        response = tkFileDialog.askopenfilename(**options)
        if response:
            self.import_button.config(state=NORMAL)
            pathVariable.set(response)

    def downloadSOFTdialog(self):
        """
        Popup a dialog box for users to enter the name of a soft file to download.
        """

        self.dsd = top = Toplevel(self)
        self.dsd.transient(self)
        Label(top, text="SOFT file number(GDS####.soft.gz)").pack()
        self.dsd_value= e = Entry(top)
        e.pack()
        b = Button(top, text="Download", command=self.downloadSOFT)
        b.pack()

        top.geometry("+%d+%d" % (self.winfo_rootx()+50,
                                  self.winfo_rooty()+50))


        top.wait_window(self)


    def downloadSOFT(self):
        softnumber = self.dsd_value.get().strip()
        if re.match(r'\d{4}',softnumber) is None or len(softnumber) != 4:
            tkMessageBox.showerror(message="Invalid SOFT file number.")
            return

        softfile = 'GDS' + softnumber + '.soft.gz' 
        from urllib2 import URLError
        try:
            result = self.root.controller.downloadSOFT(softfile)
        except URLError, e:
            tkMessageBox.showerror(title="Download Error", message=(str(e)))
            return

        self.dsd.destroy()
        if result is not None:
            insert = True
            self.import_button.config(state=NORMAL)
            for path in self.softFilePath:
                if len(path.get().strip()) == 0:
                    path.set(result)
                    insert = False
            if insert:#need to add a new browse box
                self.softfileadd()
                self.softFilePath[-1].set(result)
        else:
            tkMessageBox.showerror(message="Download unsuccessful.")

    def gnfiledialog(self):
        file_opt = options =  {}
        if platform.platform()[0:3] != 'Dar':#mac no like 
            options['filetypes'] = [('Gene Matrix Transposed file format', '.gmt')]
        options['parent'] = self
        options['initialdir'] = 'data'
        options['initialfile'] = 'c2.biocarta.v2.5.symbols.gmt'
        options['title'] = "AUREA - Select network file."
        response = tkFileDialog.askopenfilename(**options)
        if response:
           self.import_button.config(state=NORMAL)
           self.gnPath.set(response)

    def gsynfiledialog(self):
        file_opt = options =  {}
        if platform.platform()[0:3] != 'Dar':
            options['filetypes'] = [('NCBI gene_info file', '.gz')]
        options['parent'] = self
        options['initialdir'] = 'data'
        options['initialfile'] = 'Homo_sapiens.gene_info.gz'
        options['title'] = "AUREA - Select synonym file."
        response = tkFileDialog.askopenfilename(**options)
        if response:
            self.import_button.config(state=NORMAL)
            self.gsynPath.set(response)
    
    @run_in_thread
    @thread_error_catch
    def importFiles(self):
        """
        Imports the files.
        called by importFiles
        """
        if self.checkFiles():
            self.root.controller.unloadFiles()
            self.import_button.config(state=DISABLED)
            for path in self.softFilePath:
                self.root.controller.addSOFTFile(path.get()) 
            self.root.controller.setGeneNetworkFile(self.gnPath.get())
            self.root.controller.setSynonymFile(self.gsynPath.get())
            self.root.controller.loadFiles()
            #update states
            self.root.controller.updateState(self.remote.DataImport, 1)
            ni = self.root.controller.getNetworkInfo()
            if ni is not None:
                self.root.controller.updateState(self.remote.NetworkImport, 1)
           
    def disableButtons(self):
        """
        disables all buttons
        """
        self.remote.disableAllButtons()
        for b in self.buttonList:
            b.config(state=DISABLED)

        for b in self.softFileDialogButton:
            b.config(state=DISABLED)

        for b in  self.softFileDeleteButton:
            b.config(state=DISABLED)

    def enableButtons(self):
        """
        Enables the all(valid) buttons
        """
        for b in self.buttonList:
            b.config(state=NORMAL)
        
        for b in self.softFileDialogButton:
            b.config(state=NORMAL)

        for b in  self.softFileDeleteButton:
            b.config(state=NORMAL)
        self.remote.stateChange()

 
    def checkFiles(self):
        """
        Makes sure we have the necessary info to perform import
        """
        import os.path
        goodFiles = True
        for path in self.softFilePath:
            if not os.path.exists(path.get()):
                goodFiles = False
        if not goodFiles:
           tkMessageBox.showerror(message="SOFT file path is invalid")
           return False
        if not os.path.exists(self.gnPath.get()) and len(self.gnPath.get()) > 0:
            tkMessageBox.showerror(message="Gene Network file path is invalid")
            return False
        if not os.path.exists(self.gsynPath.get()) and len(self.gsynPath.get()) > 0:
            tkMessageBox.showerror(message="Gene Synonym file path is invalid")
            return False
        return True

class ClassDefinitionPage(Page):
    """
    Defines the Class Definition Layout
    """
    def __init__(self, root):
        Page.__init__(self, root, 'Class')
        self.className1 = None
        self.className2 = None
        self.unclassified_listbox = None
        self.sample_list = []
        self.subset_list = []
        #a token prepended to the subset label
        self.tok = "*ss: "

    def setUpPage(self):
        self.define_button = Button(self, text="Define Classes", command=self.buildClasses)
        self.setUpClassLabelFrame()
        self.setUpClassPartitionPage()
        
    def setUpClassLabelFrame(self):
        def unlockDefine(e):
            self.define_button.config(state=NORMAL)
        self.descriptiveText = Label(self, text="Create names for the classes you will be using.")
        self.className1Label = Label(self, text="Class 1:")
        self.className2Label = Label(self, text="Class 2:")
        if self.className1 is None:
            self.className1 = StringVar()
        self.className1E = Entry(self, textvariable=self.className1, width=50)
        self.className1E.bind("<Key>", unlockDefine)
        if self.className2 is None:
            self.className2 = StringVar()
        self.className2E = Entry(self, textvariable=self.className2, width=50)
        self.className2E.bind("<Key>", unlockDefine)

    def setUpClassPartitionPage(self):
        if self._updatedSamples():
            self.className1.set('')
            self.className2.set('')
            self.sample_list = self.root.controller.getSamples()
            self.subset_list = self.root.controller.getSubsets()
            s1 = self.s1 = Scrollbar(self, orient=VERTICAL)
            self.unclassified_listbox = Listbox(self, yscrollcommand=s1.set)
            s1.config(command=self.unclassified_listbox.yview)
            maxlen = 0
            #add subsets to unclassified listbox
            for subset_desc, _ in self.subset_list:
                txt = self.tok + subset_desc
                if len(txt) > maxlen:
                    maxlen = len(txt)
                self.unclassified_listbox.insert(END, txt)
            #add samples to unclassified listbox
            for sample in self.sample_list:
                if len(sample) > maxlen:
                    maxlen = len(sample)
                self.unclassified_listbox.insert(END, sample)
            self.unclassified_listbox.config(width=maxlen)
            s2 = self.s2 = Scrollbar(self, orient=VERTICAL)
     
            self.class1listbox = Listbox(self, width=maxlen, yscrollcommand=s2.set)
            s2.config(command=self.class1listbox.yview)
            self.class1addbutton = Button(self,text="<", command=self.add1)
            self.class2addbutton = Button(self,text=">", command=self.add2)
            self.class1removebutton = Button(self, text=">", command = self.rem1)
            self.class2removebutton = Button(self, text="<", command = self.rem2) 
            s3 = self.s3 = Scrollbar(self, orient=VERTICAL)
            self.class2listbox = Listbox(self, width=maxlen, yscrollcommand=s3.set)
            s3.config(command=self.class2listbox.yview)
            self.unclassifiedLabel = Label(self, text="Select Training Set")
            self.description=Text(self,height=10,width=50,background='white')
            self.define_button.config(state=NORMAL)
        else:
            self.define_button.config(state=DISABLED)

    def drawPage(self):
        self.setAppTitle("Class Definition")
        #draw Labels        
        self.className1Label.grid(row=0,column=0, sticky=E)
        self.className1E.grid(row=0,column=1, columnspan=2, sticky=W)
        self.unclassifiedLabel.grid(row=0, column=4)
        self.columnconfigure( 1, weight = 1 )
        self.className2Label.grid(row=0, column=7, sticky=E)
        self.className2E.grid(row=0,column=8,columnspan=2,sticky=W)
        self.columnconfigure( 8, weight = 1 )
        #draw partitioner
        self.class1listbox.grid(row=1,rowspan=2, column=0, columnspan=2, sticky=N+S+E+W)
        self.s2.grid(row=1, rowspan=2,column=2,sticky=N+S)
        self.class1addbutton.grid(row=1, column=3)
        self.unclassified_listbox.grid(row=1,rowspan=2, column=4, sticky=N+S+E+W)
        self.s1.grid(row=1, rowspan=2,column=5,sticky=N+S)
        self.class2addbutton.grid(row=1, column=6)
        self.class2listbox.grid(row=1,rowspan=2, column=7, columnspan=2, sticky=N+S+E+W)
        self.s3.grid(row=1, rowspan=2,column=9,sticky=N+S)
        

        self.class1removebutton.grid(row=2, column=3)
        self.class2removebutton.grid(row=2, column=6)
        #description
        self.description.grid(row=3,column=0, columnspan=10, sticky=N+S+E+W)
        self.description.config(state=DISABLED)
        self.current = None
        self.poll()

        self.define_button.grid(row=4, column=4, columnspan=6, sticky=E+W )        
        self.grid(row=1,column=1, sticky=N+S+E+W)
        numcolumns, numrows = self.grid_size()
        #self.rowconfigure(numrows-1 , weight = 0 )
        self.rowconfigure(1, weight = 1 )
        self.rowconfigure(2, weight = 1 )
        self.columnconfigure( 4, weight = 1 )

    def _isSubsetLabel(self, txt):
        """
        Returns whether the txt contains the token defined in setUpClassPartitionPage
        """
        return txt[:len(self.tok)] == self.tok
            

    def _updatedSamples(self):
        """
        Check if the sample list has changed
        (True if we need to clear samples)
        Note this returns True on initialization
        """
        new_sample_list = self.root.controller.getSamples()
        c = self.root.controller
        ci =c.getClassificationInfo()
        if ci[1] == 0:
            return True
        if len(new_sample_list) != len(self.sample_list):
            return True
        for i, sample in enumerate(new_sample_list):
            if sample != self.sample_list[i]:
                return True

        return False
        
 
    def move(self, origin, dest):
        self.define_button.config(state=NORMAL)
        if len(origin.curselection()) > 0:
            current = origin.curselection()
            try:
                current = map(int, current)
            except ValueError:
                pass
            if origin.get(current[0])[:len(self.tok)] != self.tok:
                #not a subset
                current.sort()
                current.reverse()
                
                for f in current:
                    self._swap(origin, dest, f)
                    origin.selection_set(int(f))
            else:
                #subset 
                self.moveSubset(origin, dest, origin.get(current[0])[len(self.tok):])

    def _swap(self, origin, dest, f):
        """
        Moves the value at the given index to the destination
        """
        val = origin.get(f)
        origin.delete(f)
        dest.insert(END, val )

    def moveSubset(self, origin, dest, subsetLabel):
        values = origin.get(0,END)
        delIndices = []
        sssampleList = self._subsetSampleList(subsetLabel)
        sssampleDict = {}
        for x in sssampleList:
            sssampleDict[x] = True
        sslIndex = 0
        for i, val in enumerate(values):
            if val in sssampleDict:
                dest.insert(END, val)
                delIndices.append(i)
            elif val[len(self.tok):] == subsetLabel:
                delIndices.append(i)
                dest.insert(0, self.tok + subsetLabel)
        delIndices.reverse()
        for i in delIndices:
            origin.delete(i)
        origin.selection_set(delIndices[-1])

      
    def add1(self):
        self.move(self.unclassified_listbox, self.class1listbox)
        self.current = None

    def add2(self):
        self.move(self.unclassified_listbox, self.class2listbox)
        self.current = None

    def rem1(self):
        self.move( self.class1listbox,self.unclassified_listbox)

    def rem2(self):
        self.move( self.class2listbox,self.unclassified_listbox)

    def poll(self):
        now, lbox = self._currentList()   
        if self.current != (now, lbox):
            self.displayDescription(now, lbox)
            self.current = (now, lbox)
        self.after(250, self.poll)

    def _currentList(self):
        """
        Returns a 2-tuple
        (tuple containing selected, currently selected listbox object)
        """
        uncList = self.unclassified_listbox.curselection()
        c1List = self.class1listbox.curselection()
        c2List = self.class2listbox.curselection()
        now = tuple()
        lb = None
        if len(uncList) > 0:
            now = uncList
            lb = self.unclassified_listbox
        if len(c1List) > 0:
            now = c1List
            lb = self.class1listbox
        if len(c2List) > 0:
            now = c2List
            lb = self.class2listbox
        return (now, lb)
         
    def _subsetDescription(self, subsetLabel):
        mystr = "Subset: " + subsetLabel[len(self.tok):]
        mystr += os.linesep
        mystr += "Contains samples: " 
        mystr += ' : '.join(self._subsetSampleList(subsetLabel[len(self.tok):]))
        return mystr

    def _subsetSampleList(self, subsetLabel):
        for d, l in self.subset_list:
            if d == subsetLabel:
                return l
 
    def displayDescription(self, cursor, listbox):
        if len(cursor) > 0:
            text = "No Description Available"
            raw = listbox.get(int(cursor[0]))
            if self._isSubsetLabel(raw):
                text = self._subsetDescription(raw)
            else:
                a = raw.split('].')
                table = a[0][1:]
                sample_id = a[1].strip()
                text = self.root.controller.getSampleInfo(table, sample_id)
            self.description.config(state=NORMAL)
            self.description.delete(1.0, END)
            self.description.insert(END, text)
            self.description.config(state=DISABLED)

    def buildClasses(self):
        if (len(self.className1.get().strip()) == 0 or len(self.className2.get().strip()) == 0):
           tkMessageBox.showerror(message="You must enter labels for the classes.")
           return False
        if self.class1listbox.size() == 0 or self.class2listbox.size() == 0:
           tkMessageBox.showerror(message="Each class must have at least one label.")
           return False
        self.root.controller.createClassification(self)
        class1 = []
        class2 = []
        for i in xrange(self.class1listbox.size()):
            if not self._isSubsetLabel(self.class1listbox.get(i)):
                raw = self.class1listbox.get(i).split('].')
                table = raw[0][1:]
                sample_name = raw[1]
                class1.append((table, sample_name))
        
        for i in xrange(self.class2listbox.size()):
            if not self._isSubsetLabel(self.class2listbox.get(i)):
                raw = self.class2listbox.get(i).split('].')
                table = raw[0][1:]
                sample_name = raw[1]
                class2.append((table, sample_name))
        self.root.controller.partitionClasses(class1, class2)
        
        self.define_button.config(state=DISABLED)
        self.root.controller.updateState(self.remote.ClassCreation, 1)

        return True

    def clearPage(self):
        self.clearGrid()
        self.grid_forget()
        

class LearnerSettingsPage(Page):
    def __init__(self, root):
        Page.__init__(self, root, 'Settings')

    def setUpPage(self):
        m = self.root.menu
        a = self.descLabel = Label(self, text="Choose the settings for the Learning algorithms.")
        a1 = self.noteLabel = Label(self, text="Note: You can save your current settings or load previously saved settings from the File menu option.")
        self._italicFont(a1)            
        b = self.diracButton = Button(self, text="Dirac...", command=m.dirac_settings)
        c = self.tspButton = Button(self, text="TSP...", command=m.tsp_settings)
        d = self.ktspButton = Button(self, text="k-TSP...", command=m.ktsp_settings)
        e = self.tstButton = Button(self, text="TST...", command=m.tst_settings)
        f = self.adaptiveButton = Button(self, text="Adaptive...", command=m.adaptive_settings)
        self.l = [a, a1,b,c,d,e,f]

    def drawPage(self):
        self.setAppTitle("Learner Settings")
        for i, button in enumerate(self.l):
            button.grid(row=i, column=0, padx=20, pady=10, sticky=E+W)
            self.rowconfigure(i, weight = 1 )

    def clearPage(self):
        self.clearGrid()
        self.grid_forget()
 
class TrainClassifiers(Page):
    def __init__(self, root):
        Page.__init__(self, root, 'Train')
        self.auto_target_acc = None
        self.auto_maxtime = None
        

    def drawPage(self):
        self.setAppTitle("Train Classifiers")

        self.training_label.grid(row=0, column=0, columnspan=2)
        self.tsp_button.grid(row=1, column=0)
        self.ktsp_button.grid(row=2, column=0)
        self.tst_button.grid(row=3, column=0)
        self.dirac_button.grid(row=4, column=0)
        self.auto_button.grid(row=5, column=0)


        self.target_message.grid(row=6, column=0, columnspan=2)
        self.auto_maxtimeE.grid(row=7,column=1)
        self.auto_maxtime_label.grid(row=7, column=0)
        self.auto_target_acc_label.grid(row=8, column=0)
        self.auto_target_accE.grid(row=8, column=1)

        for x in self.buttonList:
            x.grid(sticky=E+W)
        for x in range(9):
            self.rowconfigure(x, weight = 1 )
    
    def setUpPage(self):
        s = self
        s.training_label= Label(self, text="Please click a button for the algorithm you would like to train.")
        a=s.dirac_button = Button(self, text="Train Dirac...", command=self.trainDirac )
        b=s.tsp_button = Button(self, text="Train TSP...", command= self.trainTSP )
        c=s.ktsp_button = Button(self, text="Train k-TSP...", command=self.trainKTSP )
        d=s.tst_button = Button(self, text="Train TST...", command=self.trainTST )
  
        e=s.auto_button = Button(self, text="Adaptive Training...", command=self.trainAdaptive )
        s.auto_target_acc_label = Label(self, text="Target Accuracy:")
        s.auto_maxtime_label = Label(self, text="Maximum Time(sec):")
        if s.auto_maxtime is None:
            s.auto_maxtime = StringVar()
        if s.auto_target_acc is None:
            s.auto_target_acc = StringVar()
        s.auto_maxtimeE = Entry(self, textvariable=self.auto_maxtime) 
        s.auto_target_accE = Entry(self, textvariable=s.auto_target_acc)
        s.dirac_warning = Label(self, text="Gene Network file required", fg="red")
        s.adaptive_warning = Label(self, text="Gene Network file required", fg="red")
        s.target_message = Label(self, text="Please specify max time & target accuracy for Adaptive", fg="red")
        s.buttonList = [a,b,c,d,e]

    def disableButtons(self):
        """
        disables all buttons
        """
        self.remote.disableAllButtons()
        for b in self.buttonList:
            b.config(state=DISABLED)

    def enableButtons(self):
        """
        Enables the all(valid) buttons
        """
        def netLoaded():
            m = self.remote
            nisat = m.getDepVector([m.NetworkImport])
            return m.dependenciesSatisfied(self.root.controller.dependency_state, nisat)

        for b in self.buttonList:
            b.config(state=NORMAL)

        if not netLoaded():
            self.dirac_warning.grid(row=4, column=1)
            self.adaptive_warning.grid(row=5, column=1)
            self.dirac_button.config(state=DISABLED)
            self.auto_button.config(state=DISABLED)
        else:
            self.dirac_button.config(state=NORMAL)
            self.auto_button.config(state=NORMAL)
            self.remote.stateChange()

    @run_in_thread
    @thread_error_catch
    def trainDirac(self):
        self.root.controller.trainDirac()
        self.root.controller.updateState(self.remote.TrainDirac, 1)
        self.root.controller.updateState(self.remote.TrainAny, 1)
        self.thread_message_queue.put(('diracResult',None))

    @run_in_thread
    @thread_error_catch
    def trainTSP(self):
        self.root.controller.trainTSP()
        self.root.controller.updateState(self.remote.TrainTSP, 1)
        self.root.controller.updateState(self.remote.TrainAny, 1)
        self.thread_message_queue.put(('tspResult',None))


    @run_in_thread
    @thread_error_catch
    def trainKTSP(self):
        self.root.controller.updateState(self.remote.TrainKTSP, 1)
        self.root.controller.updateState(self.remote.TrainAny, 1)
        self.root.controller.trainkTSP()
        self.thread_message_queue.put(('ktspResult',None))

       
    @run_in_thread
    @thread_error_catch
    def trainTST(self):
        self.root.controller.trainTST()
        self.root.controller.updateState(self.remote.TrainTST, 1)
        self.root.controller.updateState(self.remote.TrainAny, 1)
        self.thread_message_queue.put(('tstResult',None))


       

    @run_in_thread
    @thread_error_catch
    def trainAdaptive(self):
        if self.adaptiveGood():
            self.root.controller.trainAdaptive(self.auto_target_acc.get(), self.auto_maxtime.get())
            self.root.controller.updateState(self.remote.TrainAdaptive, 1)
            self.root.controller.updateState(self.remote.TrainAny, 1)
            self.thread_message_queue.put(('adaptiveResult',None))
           
    def clearPage(self):
        self.clearGrid()
        self.grid_forget()

class TestClassifiers(Page):
    """
    Displays a list of unclassified samples and allows you to choose one 
    for classification,
    """

    def __init__(self, root):
        Page.__init__(self, root, 'Test')
        self.className1 = None
        self.className2 = None
        self.unclassified_listbox = None
        self.sample_list = []
        self.subset_list = []
        self.buttonList = []
        self.navButtonList = []
        self.partition_queue = Queue.Queue()
        self.results_queue = Queue.Queue()
        #a token prepended to the subset label
        self.tok = "*ss: "
        self.classified_results = None
        self.results_lock = threading.Lock()
        self.curr_learner = None

    def setUpPage(self):
        """
        Called when you enter page
        """
        self.setUpClassifyFrame()
        self.setUpClassPartitionPage()

    def setUpClassifyFrame(self):
        s = self
        if self.className1 is None:
            self.className1 = StringVar()
        if self.className2 is None:
            self.className2 = StringVar()
        self.className1Label = Label(self, textvariable=self.className1)
        self.className2Label = Label(self, textvariable=self.className2)
        #putting buttons into a subframe
        sf =self.subFrame = Frame(self)
        s.classify_label= Label(sf, text="Select method.")
        a=s.dirac_button = Button(sf, text="Dirac...", command=self.classifyDirac )
        b=s.tsp_button = Button(sf, text="TSP...", command= self.classifyTSP )
        c=s.ktsp_button = Button(sf, text="k-TSP...", command=self.classifyKTSP )
        d=s.tst_button = Button(sf, text="TST...", command=self.classifyTST )
        e=s.adaptive_button = Button(sf, text="Adaptive...", command=self.classifyAdaptive )
        self.buttonList= [a,b,c,d,e]
       
    def setUpClassPartitionPage(self):
        if self._updatedSamples():
            cname1, _, cname2, _ =  self.root.controller.getClassificationInfo()
            self.className1.set(cname1)
            self.className2.set(cname2)
            self.sample_list = self.root.controller.getUntrainedSamples()
            self.subset_list = self.root.controller.getSubsets()
            s1 = self.s1 = Scrollbar(self, orient=VERTICAL)
            self.unclassified_listbox = Listbox(self, yscrollcommand=s1.set)
            s1.config(command=self.unclassified_listbox.yview)
            maxlen = 0
            #add subsets to unclassified listbox
            for subset_desc, _ in self.subset_list:
                txt = self.tok + subset_desc
                if len(txt) > maxlen:
                    maxlen = len(txt)
                self.unclassified_listbox.insert(END, txt)
            #add samples to unclassified listbox
            for sample in self.sample_list:
                if len(sample) > maxlen:
                    maxlen = len(sample)
                self.unclassified_listbox.insert(END, sample)
            self.unclassified_listbox.config(width=maxlen)
            s2 = self.s2 = Scrollbar(self, orient=VERTICAL)
     
            self.class1listbox = Listbox(self, width=maxlen, yscrollcommand=s2.set)
            s2.config(command=self.class1listbox.yview)
            a=self.class1addbutton = Button(self,text="<", command=self.add1)
            b=self.class2addbutton = Button(self,text=">", command=self.add2)
            c=self.class1removebutton = Button(self, text=">", command = self.rem1)
            d=self.class2removebutton = Button(self, text="<", command = self.rem2) 
            self.navButtonList = [a,b,c,d]
            s3 = self.s3 = Scrollbar(self, orient=VERTICAL)
            self.class2listbox = Listbox(self, width=maxlen, yscrollcommand=s3.set)
            s3.config(command=self.class2listbox.yview)
            self.unclassifiedLabel = Label(self, text="Select Partitioning")
            self.description=Text(self,height=10,width=50,background='white')
        self.enableLearnersButtons()

    def disableLearnersButtons(self):
        """
        Disables the learners button
        """
        for button in self.buttonList:
            button.config(state=DISABLED)

    def enableLearnersButtons(self):
        """
        enables the learners button
        """
        if self.root.controller.dirac is not None:
            self.dirac_button.config(state=NORMAL)
        else:
            self.dirac_button.config(state=DISABLED)

        if self.root.controller.tsp is not None:
            self.tsp_button.config(state=NORMAL)
        else:
            self.tsp_button.config(state=DISABLED)


        if self.root.controller.ktsp is not None:
            self.ktsp_button.config(state=NORMAL)
        else:
            self.ktsp_button.config(state=DISABLED)

       
        if self.root.controller.tst is not None:
            self.tst_button.config(state=NORMAL)
        else:
            self.tst_button.config(state=DISABLED)

        if self.root.controller.adaptive is not None:
            self.adaptive_button.config(state=NORMAL)
        else:
            self.adaptive_button.config(state=DISABLED)

    def drawPage(self):
        self.setAppTitle("Test Classifiers")
        #draw Labels        
        self.className1Label.grid(row=0,column=0, sticky=E)
        self.unclassifiedLabel.grid(row=0, column=4)
        self.columnconfigure( 1, weight = 1 )
        self.className2Label.grid(row=0, column=7, sticky=E)
        self.columnconfigure( 8, weight = 1 )
        #draw partitioner
        self.class1listbox.grid(row=1,rowspan=2, column=0, columnspan=2, sticky=N+S+E+W)
        self.s2.grid(row=1, rowspan=2,column=2,sticky=N+S)
        self.class1addbutton.grid(row=1, column=3)
        self.unclassified_listbox.grid(row=1,rowspan=2, column=4, sticky=N+S+E+W)
        self.s1.grid(row=1, rowspan=2,column=5,sticky=N+S)
        self.class2addbutton.grid(row=1, column=6)
        self.class2listbox.grid(row=1,rowspan=2, column=7, columnspan=2, sticky=N+S+E+W)
        self.s3.grid(row=1, rowspan=2,column=9,sticky=N+S)
        

        self.class1removebutton.grid(row=2, column=3)
        self.class2removebutton.grid(row=2, column=6)
        #description
        self.description.grid(row=3,column=0, columnspan=10, sticky=N+S+E+W)
        self.description.config(state=DISABLED)
        self.current = None
        self.poll()

        self.grid(row=1,column=1, sticky=N+S+E+W)
        numcolumns, numrows = self.grid_size()
        self.subFrame.grid(row=1, rowspan=numrows-1, column=numcolumns, sticky=N+S+E+W)
        self.classify_label.grid(row=0, column=0, sticky=E+W)
        self.dirac_button.grid(row=4, column=0, sticky=E+W)
        self.tsp_button.grid(row=1, column=0, sticky=E+W)
        self.tst_button.grid(row=3, column=0, sticky=E+W)
        self.ktsp_button.grid(row=2, column=0, sticky=E+W)
        self.adaptive_button.grid(row=5, column=0, sticky=E+W)
        for i in range(7):
            self.rowconfigure(i, weight=1)
        self.current = None
        self.poll()

    def disableButtons(self):
        self.disableLearnersButtons()
        for b in self.navButtonList:
            b.config(state=DISABLED)
        self.remote.disableAllButtons()

    def enableButtons(self):
        self.enableLearnersButtons()
        for b in self.navButtonList:
            b.config(state = NORMAL)
        self.remote.stateChange()

    def _isSubsetLabel(self, txt):
        """
        Returns whether the txt contains the token defined in setUpClassPartitionPage
        """
        return txt[:len(self.tok)] == self.tok


    def _updatedSamples(self):
        """
        Check if the sample list has changed
        (True if we need to clear samples)
        Note this returns True on initialization
        """
        new_sample_list = self.root.controller.getUntrainedSamples()
        c = self.root.controller
        c1name,c1Len, c2name,c2Len  = c.getClassificationInfo()
        if self.className1 is None:
            #initialize
            return True
        if self.className1.get() != c1name or self.className2.get() != c2name:
            #change
            return True
        if len(new_sample_list) != len(self.sample_list):
            #change
            return True
        for i, sample in enumerate(new_sample_list):
            if sample != self.sample_list[i]:
                #change
                return True
        #classes have not changed
        return False
        
 
    def move(self, origin, dest):
        if len(origin.curselection()) > 0:
            current = origin.curselection()
            try:
                current = map(int, current)
            except ValueError:
                pass
            if origin.get(current[0])[:len(self.tok)] != self.tok:
                #not a subset
                current.sort()
                current.reverse()
                
                for f in current:
                    self._swap(origin, dest, f)
                    origin.selection_set(int(f))
            else:
                #subset 
                self.moveSubset(origin, dest, origin.get(current[0])[len(self.tok):])

    def _swap(self, origin, dest, f):
        """
        Moves the value at the given index to the destination
        """
        val = origin.get(f)
        origin.delete(f)
        dest.insert(END, val )

    def moveSubset(self, origin, dest, subsetLabel):
        values = origin.get(0,END)
        delIndices = []
        sssampleList = self._subsetSampleList(subsetLabel)
        sssampleDict = {}
        for x in sssampleList:
            sssampleDict[x] = True
        sslIndex = 0
        for i, val in enumerate(values):
            if val in sssampleDict:
                dest.insert(END, val)
                delIndices.append(i)
            elif val[len(self.tok):] == subsetLabel:
                delIndices.append(i)
                dest.insert(0, self.tok + subsetLabel)
        delIndices.reverse()
        for i in delIndices:
            origin.delete(i)
        origin.selection_set(delIndices[-1])

      
    def add1(self):
        self.move(self.unclassified_listbox, self.class1listbox)
        self.current = None

    def add2(self):
        self.move(self.unclassified_listbox, self.class2listbox)
        self.current = None

    def rem1(self):
        self.move( self.class1listbox,self.unclassified_listbox)

    def rem2(self):
        self.move( self.class2listbox,self.unclassified_listbox)

    def poll(self):
        now, lbox = self._currentList()   
        if self.current != (now, lbox):
            self.displayDescription(now, lbox)
            self.current = (now, lbox)
        self.after(250, self.poll)

    def _currentList(self):
        """
        Returns a 2-tuple
        (tuple containing selected, currently selected listbox object)
        """
        uncList = self.unclassified_listbox.curselection()
        c1List = self.class1listbox.curselection()
        c2List = self.class2listbox.curselection()
        now = tuple()
        lb = None
        if len(uncList) > 0:
            now = uncList
            lb = self.unclassified_listbox
        if len(c1List) > 0:
            now = c1List
            lb = self.class1listbox
        if len(c2List) > 0:
            now = c2List
            lb = self.class2listbox
        return (now, lb)
         
    def _subsetDescription(self, subsetLabel):
        mystr = "Subset: " + subsetLabel[len(self.tok):]
        mystr += os.linesep
        mystr += "Contains samples: " 
        mystr += ' : '.join(self._subsetSampleList(subsetLabel[len(self.tok):]))
        return mystr

    def _subsetSampleList(self, subsetLabel):
        for d, l in self.subset_list:
            if d == subsetLabel:
                return l
 
    def displayDescription(self, cursor, listbox):
        if len(cursor) > 0:
            text = "No Description Available"
            raw = listbox.get(int(cursor[0]))
            if self._isSubsetLabel(raw):
                text = self._subsetDescription(raw)
            else:
                a = raw.split('].')
                table = a[0][1:]
                sample_id = a[1].strip()
                text = self.root.controller.getSampleInfo(table, sample_id)
            self.description.config(state=NORMAL)
            self.description.delete(1.0, END)
            self.description.insert(END, text)
            self.description.config(state=DISABLED)


    def clearPage(self):
        self.clearGrid()
        self.grid_forget()

    def addUnc(self, table, sample):
        self.root.controller.addUnclassified(table, sample)


    def partition(self):
        class1 = []
        class2 = []
        for i in xrange(self.class1listbox.size()):
            if not self._isSubsetLabel(self.class1listbox.get(i)):
                raw = self.class1listbox.get(i).split('].')
                table = raw[0][1:]
                sample_name = raw[1]
                class1.append((table, sample_name))
        
        for i in xrange(self.class2listbox.size()):
            if not self._isSubsetLabel(self.class2listbox.get(i)):
                raw = self.class2listbox.get(i).split('].')
                table = raw[0][1:]
                sample_name = raw[1]
                class2.append((table, sample_name))
        return (class1, class2)

    def fillClassifyQueue(self):
        class1, class2 = self.partition()
        for table,sample in class1:
            self.partition_queue.put( (0,table, sample) )
        for table, sample in class2:
            self.partition_queue.put( (1,table, sample) )
        with self.results_lock:
            self.hRon = True
        #turn on results handling
        self.handleResults()

    def displayResults(self):
        if self.curr_learner == 'dirac':
            self.thread_message_queue.put(('statusbarclear', None))
            DiracClassificationResults(self)
        elif self.curr_learner == 'tsp':
            self.thread_message_queue.put(('statusbarclear', None))
            TSPClassificationResults(self)
        elif self.curr_learner == 'tst':
            self.thread_message_queue.put(('statusbarclear', None))
            TSTClassificationResults(self)
        elif self.curr_learner == 'ktsp':
            self.thread_message_queue.put(('statusbarclear', None))
            KTSPClassificationResults(self)
        elif self.curr_learner == 'adaptive':
            self.thread_message_queue.put(('statusbarclear', None))
            AdaptiveClassificationResults(self)

    def handleResults(self):
        """
        Receives results from learner as they are finished
        """
        
        def getNames(pred, act):
            #helper-returns string names for
            #(predicted class name, actual class name)
            c1name = self.className1.get()
            c2name = self.className2.get()
            if pred == 0:
                predname = c1name
            else:
                predname = c2name
            if act == 0:
                actname = c1name
            else:
                actname = c2name
            return (predname, actname)

        while not self.results_queue.empty():
            pred, act, table, sample = self.results_queue.get()
            predname, actualname = getNames(pred, act)
            msg = sample + " classified as " + predname
            if pred == act:
                msg += " : Correct"
            else:
                msg += " : Incorrect, was " + actualname
            self.thread_message_queue.put( ('statusbarset', msg) ) 
            self.classified_results.append( (pred, act, table, sample) )
        with self.results_lock:
            if self.hRon:
                self.after(500, self.handleResults)

    def classifyDirac(self):
        if self.root.controller.dirac is not None:
            self.curr_learner = 'dirac'
            self.root.controller.dirac_classified_results=[]

            self.classified_results = self.root.controller.dirac_classified_results
            self.fillClassifyQueue()
            self.threadedClassifyDirac()


    @run_in_thread
    @thread_error_catch
    def threadedClassifyDirac(self):       
        while not self.partition_queue.empty():
            classNum, table, sample = self.partition_queue.get()
            self.addUnc(table,sample)
            msg = "Dirac classifying " + sample
            self.thread_message_queue.put( ( 'statusbarset', msg) )
            classification = self.root.controller.classifyDirac()
            self.results_queue.put((classification, classNum, table, sample))
        self.thread_message_queue.put( ('classifyComplete',None) )
     
    def classifyTSP(self):
        if self.root.controller.tsp is not None:
            self.curr_learner = 'tsp'
            self.root.controller.tsp_classified_results=[]
            self.classified_results = self.root.controller.tsp_classified_results
            self.fillClassifyQueue()
            self.threadedClassifyTSP()

    @run_in_thread
    @thread_error_catch
    def threadedClassifyTSP(self):
        while not self.partition_queue.empty():
            classNum, table, sample = self.partition_queue.get()
            self.addUnc(table,sample)
            msg = "TSP classifying " + sample
            self.thread_message_queue.put( ( 'statusbarset', msg) )
            classification = self.root.controller.classifyTSP()
            self.results_queue.put((classification, classNum, table, sample))
        self.thread_message_queue.put( ('classifyComplete',None) )
                
    def classifyKTSP(self):
        if self.root.controller.ktsp is not None:
            self.curr_learner = 'ktsp'
            self.root.controller.ktsp_classified_results=[]
            self.classified_results = self.root.controller.ktsp_classified_results
            self.fillClassifyQueue()
            self.threadedClassifyKTSP()

    @run_in_thread
    @thread_error_catch
    def threadedClassifyKTSP(self):
        while not self.partition_queue.empty():
            classNum, table, sample = self.partition_queue.get()
            self.addUnc(table,sample)
            msg = "KTSP classifying " + sample
            self.thread_message_queue.put( ( 'statusbarset', msg) )
            classification = self.root.controller.classifykTSP()
            self.results_queue.put((classification, classNum, table, sample))
        self.thread_message_queue.put( ('classifyComplete',None) )
     
     
    def classifyTST(self):
        if self.root.controller.tst is not None:
            self.curr_learner = 'tst'
            self.root.controller.tst_classified_results=[]
            self.classified_results = self.root.controller.tst_classified_results
            self.fillClassifyQueue()
            self.threadedClassifyTST()

    @run_in_thread
    @thread_error_catch
    def threadedClassifyTST(self):
        while not self.partition_queue.empty():
            classNum, table, sample = self.partition_queue.get()
            self.addUnc(table,sample)
            msg = "TST classifying " + sample
            self.thread_message_queue.put( ( 'statusbarset', msg) )
            classification = self.root.controller.classifyTST()
            self.results_queue.put((classification, classNum, table, sample))
        self.thread_message_queue.put( ('classifyComplete',None) )
         
    def classifyAdaptive(self):
        if self.root.controller.adaptive is not None:
            self.curr_learner = 'adaptive'
            self.root.controller.adaptive_classified_results=[]
            self.classified_results = self.root.controller.adaptive_classified_results
            self.fillClassifyQueue()
            self.threadedClassifyAdaptive()


    @run_in_thread
    @thread_error_catch
    def threadedClassifyAdaptive(self):
        while not self.partition_queue.empty():
            classNum, table, sample = self.partition_queue.get()
            self.addUnc(table,sample)
            msg = "Adaptive classifying " + sample
            self.thread_message_queue.put( ( 'statusbarset', msg) )
            classification = self.root.controller.classifyAdaptive()
            self.results_queue.put((classification, classNum, table, sample))
        self.thread_message_queue.put( ('classifyComplete',None) )
         

class EvaluateClassifiers(Page):
    """
    Performs k-fold cross-validation on the learners.
    """

    def __init__(self, root):
        Page.__init__(self, root, 'Evaluate')
        self.auto_target_acc = None
        self.auto_maxtime = None
        

    def setUpPage(s):
        self = s
        s.cv_label= Label(self, text="Please select the algorithm you would like to evaluate in cross validation")
        d = s.dirac_button = Button(self, text="Dirac...", command=s.cvDirac )
        a = s.tsp_button = Button(self, text="TSP...", command= s.cvTSP )
        b= s.ktsp_button = Button(self, text="k-TSP...", command=s.cvKTSP )
        c = s.tst_button = Button(self, text="TST...", command=s.cvTST )
        e = s.adaptive_button = Button(self, text="Adaptive...", command=s.cvAdaptive )
        s.auto_target_acc_label = Label(self, text="Target Accuracy:")
        s.auto_maxtime_label = Label(self, text="Maximum Time(sec):")
        if s.auto_maxtime is None:
            s.auto_maxtime = StringVar()
        s.auto_maxtimeE = Entry(self, textvariable=self.auto_maxtime) 
        if s.auto_target_acc is None:
            s.auto_target_acc = StringVar()
        s.auto_target_accE = Entry(self, textvariable=s.auto_target_acc)
        s.target_message = Label(self, text="Please specify max time & target accuracy for Adaptive", fg="red")
        s.buttonList = [a,b,c,d,e]


    def drawPage(s):
        def netLoaded():
            m = s.root.remote
            nisat = m.getDepVector([m.NetworkImport])
            return m.dependenciesSatisfied(s.root.controller.dependency_state, nisat)

        s.setAppTitle("Evaluate Performance")
        r = 0
        s.cv_label.grid(row=r, column=0, columnspan=2)
        r += 1
        for b in s.buttonList:
            b.grid(row = r, column=0, sticky = E+W)
            r += 1
        s.target_message.grid(row=r, column=0, columnspan=2)
        r += 1
        s.auto_maxtime_label.grid( row=r, column=0)
        s.auto_maxtimeE.grid(row=r, column=1) 
        r += 1
        s.auto_target_acc_label.grid(row=r, column=0)
        s.auto_target_accE.grid(row=r, column=1)
        for x in s.buttonList:
            x.grid(sticky=E+W)
        for x in range(9):
            s.rowconfigure(x, weight = 1 )
        if not netLoaded():
            s.adaptive_button.config(state=DISABLED)
            s.dirac_button.config(state=DISABLED)
        else:
            s.adaptive_button.config(state=NORMAL)
            s.dirac_button.config(state=NORMAL)

    def disableButtons(self):
        """
        disables all buttons
        """
        self.remote.disableAllButtons()
        for b in self.buttonList:
            b.config(state=DISABLED)

    def enableButtons(self):
        """
        Enables the all(valid) buttons
        """
        def netLoaded():
            m = self.remote
            nisat = m.getDepVector([m.NetworkImport])
            return m.dependenciesSatisfied(self.root.controller.dependency_state, nisat)

        for b in self.buttonList:
            b.config(state=NORMAL)

        if not netLoaded():
            self.dirac_button.config(state=DISABLED)
            self.adaptive_button.config(state=DISABLED)
        else:
            self.dirac_button.config(state=NORMAL)
            self.adaptive_button.config(state=NORMAL)
        self.remote.stateChange()

    @run_in_thread
    @thread_error_catch
    def cvDirac(self):
        self.root.controller.crossValidateDirac()
    @run_in_thread
    @thread_error_catch
    def cvTSP(self):
        self.root.controller.crossValidateTSP()
    @run_in_thread
    @thread_error_catch
    def cvKTSP(self):
        self.root.controller.crossValidateKTSP()
    @run_in_thread
    @thread_error_catch
    def cvTST(self):
        self.root.controller.crossValidateTST()
       
    @run_in_thread
    @thread_error_catch
    def cvAdaptive(self):
        if self.adaptiveGood():
            self.root.controller.crossValidateAdaptive( self.auto_target_acc.get(), self.auto_maxtime.get())

    def clearPage(self):
        self.clearGrid()
        self.grid_forget()

class Error(Exception):
    pass

class InputError(Error):
    """
    expr -- Input expression in which the error occurred
    msg -- explanation of error
    """
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

class ImplementationError(Error):
    def __init__(self, page_id, function):
        self.msg = str(page_id) + " called " + function + "without implementing it"
