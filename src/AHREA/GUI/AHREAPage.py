from Tkinter import *
import tkFileDialog
import tkMessageBox
import os
from AHREA.GUI.AHREAResults import *
class AHREAPage(Frame):
    """
    Base class for data input frames
    """
    def __init__(self, root, id):
        Frame.__init__(self, root)
        self.root = root
        self.id = id

    def drawPage(self):
        raise ImplementationError(self.id, 'drawPage')

    def setUpPage(self):
        raise ImplementationError(self.id, 'setUpPage')

    def clearPage(self):
        raise ImplementationError(self.id, 'clearPage')

    def next(self):
        raise ImplementationError(self.id, 'next')

    def prev(self):
        raise ImplementationError(self.id, 'prev')

class WelcomePage(AHREAPage):
    """
    Just some welcome text.  Prob add some copyright and such
    """
    def __init__(self, root):
        AHREAPage.__init__(self, root, 'welcome')

    def setUpPage(self):
        welcome_img = os.path.join(self.root.controller.install_dir,'AHREA', 'data', 'AHREA-logo.pgm')
        self.photo = photo = PhotoImage(file=welcome_img)
        self.label = Label(self, text="Welcome", image=photo) 
        
    def drawPage(self):
        self.label.pack()

    def clearPage(self):
        self.label.pack_forget()

    def next(self):
        return 'filebrowse'

    def prev(self):
        pass
class FileBrowsePage(AHREAPage):
    """
    Page to choose data files
    """
    def __init__(self, root):
        AHREAPage.__init__(self, root, 'filebrowse')
        self.gnPath = None
        self.softFilePath = None
        self.gsynPath = None
        #init softfile lists
        self.softFileLabel = []
        self.softFilePath = []
       
        self.softFilePathE = []
        self.softFileDialogButton = []

        self.softFileDeleteButton = []
        self.addButton = None    

    def drawPage(self):
        ypad = 3
        r = 1
        for i in range( len(self.softFileLabel) ):
            self.softFileLabel[i].grid(row=r, column=0, pady=ypad)
            self.softFilePathE[i].grid(row=r, column=1, pady=ypad)
            self.softFileDialogButton[i].grid(row=r, column=2, pady=ypad)
            if len(self.softFileLabel) != 1:
                self.softFileDeleteButton[i].grid(row=r, column=3, pady=ypad)
            r += 1
        #wish I could put this in self.
        self.addButton.grid(row=r, column=2, pady=ypad)
        r += 1 

        self.downloadButton.grid(row=r, column=2, pady=ypad)
        r += 1

        self.gnLabel.grid(row=r, column=0, pady=ypad)
        self.gnPathE.grid(row=r, column=1, pady=ypad)
        self.gnDialogButton.grid(row=r, column = 2, pady=ypad)
        r += 1

        self.gsynLabel.grid(row=r, column=0, pady=ypad)
        self.gsynPathE.grid(row=r, column=1, pady=ypad)
        self.gsynDialogButton.grid(row=r, column = 2, pady=ypad)
        
    def setUpPage(self):
        self.softFileDisplay()
        self.geneNetworkDisplay()
        #there can be only 1
        if self.addButton is None:
            self.addButton = Button(self, text="Add another file",command=self.softfileadd)
            self.downloadButton = Button(self, text="Download...", command=self.downloadSOFTdialog)
        self.geneSynonymDisplay()    

    def clearPage(self):
        for i in range(len(self.softFileLabel)):
            self.softFileLabel[i].grid_forget()
            self.softFilePathE[i].grid_forget()
            self.softFileDialogButton[i].grid_forget()  
            self.softFileDeleteButton[i].grid_forget()
        self.downloadButton.grid_forget()    
        self.gnLabel.grid_forget()
        self.gnPathE.grid_forget()
        self.gnDialogButton.grid_forget()

        self.gsynLabel.grid_forget()
        self.gsynPathE.grid_forget()
        self.gsynDialogButton.grid_forget()
        self.pack_forget()
 
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
        self.pack()

    def softfileadd(self):
        self.softFileDisplay(add=True)
        self.clearPage()
        self.drawPage()
        self.pack()
        
    def geneNetworkDisplay(self):
        self.gnLabel = Label(self, text="Gene Network File : ")
        if self.gnPath is None:
            self.gnPath = StringVar()
        self.gnPathE = Entry(self, textvariable=self.gnPath,width=50)
        self.gnDialogButton = Button(self, text = "Browse ...",command=self.gnfiledialog)

    def geneSynonymDisplay(self):
        self.gsynLabel = Label(self, text="Gene Synonym File : ")
        if self.gsynPath is None:
            self.gsynPath = StringVar()
        self.gsynPathE = Entry(self, textvariable=self.gsynPath, width=50)
        self.gsynDialogButton = Button(self, text = "Browse ...",command=self.gsynfiledialog) 
 

    def softfiledialog(self, pathVariable):
        file_opt = options =  {}
        options['filetypes'] = [('gzipped SOFT', '.soft.gz'), ('SOFT', '.soft'),('Comma Separated', '.csv')]
        options['parent'] = self
        options['initialdir'] = 'data'
        options['title'] = "AHREA - Select data file."
        response = tkFileDialog.askopenfilename(**options)
        if response:
            pathVariable.set(response)

    def downloadSOFTdialog(self):
        self.dsd = top = Toplevel(self)
        Label(top, text="SOFT file name(GDS####.soft.gz)").pack()
        self.dsd_value= e = Entry(top)
        e.pack()
        b = Button(top, text="Download", command=self.downloadSOFT)
        b.pack()

    def downloadSOFT(self):
        result = self.root.controller.downloadSOFT(self.dsd_value.get().strip())
        self.dsd.destroy()
        if result is not None:
            insert = True
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
        options['filetypes'] = [('Gene Matrix Transposed file format', '.gmt')]
        options['parent'] = self
        options['initialdir'] = 'data'
        options['title'] = "AHREA - Select network file."
        response = tkFileDialog.askopenfilename(**options)
        if response:
            self.gnPath.set(response)

    def gsynfiledialog(self):
        file_opt = options =  {}
        options['filetypes'] = [('NCBI gene_info file', '.gz')]
        options['parent'] = self
        options['initialdir'] = 'data'
        options['initialfile'] = 'Homo_sapiens.gene_info.gz'
        options['title'] = "AHREA - Select synonym file."
        response = tkFileDialog.askopenfilename(**options)
        if response:
            self.gsynPath.set(response)

    def next(self):
        import os.path
        goodFiles = True
        for path in self.softFilePath:
            if not os.path.exists(path.get()):
                goodFiles = False
        if goodFiles:
            for path in self.softFilePath:
                self.root.controller.addSOFTFile(path.get()) 
        else:
           tkMessageBox.showerror(message="SOFT file path is invalid")
           return False
        if os.path.exists(self.gnPath.get()):
            self.root.controller.setGeneNetworkFile(self.gnPath.get())
        elif len(self.gnPath.get()) > 0:
            tkMessageBox.showerror(message="Gene Network file path is invalid")
            return False
        if os.path.exists(self.gsynPath.get()):
            self.root.controller.setSynonymFile(self.gsynPath.get())
        elif len(self.gsynPath.get()) > 0:
            tkMessageBox.showerror(message="Gene Synonym file path is invalid")
            return False
        return 'fileload'

    def prev(self):
        return 'welcome'

class FileLoadPage(AHREAPage):
    """
    Page that is displayed while files are being parsed
    """
    def __init__(self, root):
        AHREAPage.__init__(self, root, 'fileload')

    def setUpPage(self):
        self.message = StringVar(value="Loading Files")
        self.label = Label(self, textvariable=self.message)
        self.label.pack()

    def drawPage(self):
        self.pack()
        self.disable_next = True

        if len(self.root.controller.datatable) == 0:
            self.root.controller.loadFiles()
        self.displayResults()
        self.disable_next = False

    def clearPage(self):
        self.label.pack_forget()
        self.pack_forget()

    def next(self):
        if self.disable_next:
            return None
        return 'classlabels'

    def displayResults(self):
        cont = self.root.controller
        res = cont.getDataPackagingResults()
        strg = "Data merging results\n"
        strg += "Table\tGene\tProbes\n"
        for table, genes, probes in res:
            strg += table + '\t' + str(genes) + '\t' + str(probes) + '\n'
        self.message.set(strg)

    def prev(self):
        if self.disable_next:
            return None
        self.root.controller.unloadFiles()
        return 'filebrowse'

class ClassLabelPage(AHREAPage):
    """
    Page to get class information.
    """
    def __init__(self, root):
        AHREAPage.__init__(self, root, 'classlabels')
        self.className1 = None
        self.className2 = None

    def setUpPage(self):
        self.descriptiveText = Label(self, text="Create names for the classes you will be using.")
        self.className1Label = Label(self, text="Class 1 name:")
        self.className2Label = Label(self, text="Class 2 name:")
        if self.className1 is None:
            self.className1 = StringVar()
        self.className1E = Entry(self, textvariable=self.className1, width=50)
        if self.className2 is None:
            self.className2 = StringVar()
        self.className2E = Entry(self, textvariable=self.className2, width=50)

    def drawPage(self):
        self.descriptiveText.grid(row=0, columnspan=2)
        self.className1Label.grid(row=1,column=0)
        self.className2Label.grid(row=2,column=0)
        self.className1E.grid(row=1,column=1) 
        self.className2E.grid(row=2,column=1) 
        self.pack()
    def clearPage(self):
        self.pack_forget()

    def next(self):
        if len(self.className1.get().strip()) == 0 or len(self.className2.get().strip()) == 0:
            self.root.status.set("You must enter labels for the classes.")

            return None
        self.root.controller.createClassification(self)
        return 'trainingset'

    def prev(self):
        return 'fileload'

class BuildTrainingSetPage(AHREAPage):
    def __init__(self, root):
        AHREAPage.__init__(self, root, 'trainingset')
        self.unclassified_listbox = None
        self.sample_list = []
    def setUpPage(self):
        self.class1Label = Label(self, text=self.root.controller.class1name)
        self.class2Label = Label(self, text=self.root.controller.class2name)
        if self._updatedSamples():
            self.sample_list = self.root.controller.getSamples()
            s1 = self.s1 = Scrollbar(self, orient=VERTICAL)
            self.unclassified_listbox = Listbox(self, yscrollcommand=s1.set)
            s1.config(command=self.unclassified_listbox.yview)
            maxlen = 0
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
            self.class1Label = Label(self, text=self.root.controller.class1name)
            self.class2Label = Label(self, text=self.root.controller.class2name)
            self.unclassifiedLabel = Label(self, text="Select Training Set")
            self.description=Text(self,height=10,width=50,background='white')

    def _updatedSamples(self):
        """
        Check if the sample list has changed
        """
        new_sample_list = self.root.controller.getSamples()
        if len(new_sample_list) != len(self.sample_list):
            return True
        for i, sample in enumerate(new_sample_list):
            if sample != self.sample_list[i]:
                return True

        return False
        
 
    def move(self, origin, dest):
        if len(origin.curselection()) > 0:
            f = origin.curselection()[0]
            val = origin.get(f)
            origin.delete(f)
            dest.insert(END, val )
            origin.selection_set(int(f))
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


    def drawPage(self):
        self.unclassified_listbox.grid(row=2,rowspan=2, column=3)
        self.s1.grid(row=2, rowspan=2,column=4,sticky=N+S)
        self.s2.grid(row=2, rowspan=2,column=1,sticky=N+S)
        self.s3.grid(row=2, rowspan=2,column=7,sticky=N+S)
        
        self.class1listbox.grid(row=2,rowspan=2, column=0)
        self.class2listbox.grid(row=2,rowspan=2, column=6)
        self.class1Label.grid(row=1, column=0)
        self.class2Label.grid(row=1, column=6)
        self.unclassifiedLabel.grid(row=1, column=3)
        self.class1addbutton.grid(row=2, column=2)
        self.class2addbutton.grid(row=2, column=5)
        self.class1removebutton.grid(row=3, column=2)
        self.class2removebutton.grid(row=3, column=5)
        self.description.grid(row=4, columnspan=7, sticky=N+S+E+W)
        self.description.config(state=DISABLED)
        self.pack()
        self.current = None
        self.poll()

    def poll(self):
        now, lbox = self._currentList()   
        if self.current != (now, lbox):
            self.displayDescription(now, lbox)
            self.current = (now, lbox)
        self.after(250, self.poll)

    def _currentList(self):
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
         

    def displayDescription(self, cursor, listbox):
        if len(cursor) > 0:
            raw = listbox.get(int(cursor[0]))
            a = raw.split('].')
            table = a[0][1:]
            sample_id = a[1].strip()
            text = self.root.controller.getSampleInfo(table, sample_id)
            self.description.config(state=NORMAL)
            self.description.delete(1.0, END)
            self.description.insert(END, text)
            self.description.config(state=DISABLED)

    def buildClasses(self):
        class1 = []
        class2 = []
        for i in xrange(self.class1listbox.size()):
            raw = self.class1listbox.get(i).split('].')
            table = raw[0][1:]
            sample_name = raw[1]
            class1.append((table, sample_name))
        
        for i in xrange(self.class2listbox.size()):
            raw = self.class2listbox.get(i).split('].')
            table = raw[0][1:]
            sample_name = raw[1]
            class2.append((table, sample_name))
        self.root.controller.partitionClasses(class1, class2)
        
    
    def clearPage(self):
        self.pack_forget()

    def next(self):
        self.buildClasses()
        return 'training'

    def prev(self):
        return 'classlabels'

class RunTraining(AHREAPage):
    def __init__(self, root):
        AHREAPage.__init__(self, root, 'training')
        self.auto_target_acc = None
        self.auto_maxtime = None

    def drawPage(self):
        self.training_label.grid(row=1, column=0, columnspan=4)
        self.dirac_button.grid(row=2, column=0)
        self.tsp_button.grid(row=2, column=1)
        self.tst_button.grid(row=2, column=2)
        self.ktsp_button.grid(row=2, column=3)
        self.auto_maxtime_label.grid(row=3, column=0)
        self.auto_maxtimeE.grid(row=3,column=1)
        self.auto_target_acc_label.grid(row=3, column=2)
        self.auto_target_accE.grid(row=3, column=3)
        self.auto_button.grid(row=3, column=4)
        self.pack()
    
    def setUpPage(self):
        s = self
        s.training_label= Label(self, text="Please click a button for the algorithm you would like to train")
        s.dirac_button = Button(self, text="Train Dirac...", command=self.trainDirac )
        s.tsp_button = Button(self, text="Train TSP...", command= self.trainTSP )
        s.ktsp_button = Button(self, text="Train k-TSP...", command=self.trainKTSP )
        s.tst_button = Button(self, text="Train TST...", command=self.trainTST )
  
        s.auto_button = Button(self, text="Adaptive Training...", command=self.trainAdaptive )
        s.auto_target_acc_label = Label(self, text="Target Accuracy:")
        s.auto_maxtime_label = Label(self, text="Maximum Time(sec):")
        if s.auto_target_acc is None:
            s.auto_target_acc = StringVar()
        s.auto_target_accE = Entry(self, textvariable=s.auto_target_acc)
        if s.auto_maxtime is None:
            s.auto_maxtime = StringVar()
        s.auto_maxtimeE = Entry(self, textvariable=self.auto_maxtime) 

    def trainDirac(self):
        self.root.controller.trainDirac()
        DiracResults(self)

    def trainTSP(self):
        self.root.controller.trainTSP()
        TSPResults(self) 

    def trainKTSP(self):
        self.root.controller.trainkTSP()
        KTSPResults(self)
        

    def trainTST(self):
        self.root.controller.trainTST()
        TSTResults(self)

    def trainAdaptive(self):
        self.root.controller.trainAdaptive(self.auto_target_acc.get(), self.auto_maxtime.get())
    
    def clearPage(self):
        self.pack_forget()
    def next(self):
        return 'addUnclassified'
    def prev(self):
        return 'trainingset'


class addUnclassified(AHREAPage):
    """
    Displays a list of unclassified samples and allows you to choose one 
    for classification,
    """

    def __init__(self, root):
        AHREAPage.__init__(self, root, 'addUnclassified')

    def setUpPage(self):
        self.sample_list = self.root.controller.getUntrainedSamples()
        self.unclassified_listbox = Listbox(self)
        maxlen = 0
        for sample in self.sample_list:
            if len(sample) > maxlen:
                maxlen = len(sample)
            self.unclassified_listbox.insert(END, sample)
        self.unclassified_listbox.config(width=maxlen)
        self.unclassifiedLabel = Label(self, text="Select Sample for Classification")
        self.description = Text(self, height=10,width=50,background='white')
        
     
    def poll(self):
        now = self.unclassified_listbox.curselection()
        if self.current != now:
            self.displayDescription(now)
            self.current = now
        self.after(250, self.poll)

    def displayDescription(self, cursor):
        if len(cursor) > 0:
            raw = self.unclassified_listbox.get(int(cursor[0]))
            a = raw.split('].')
            table = a[0][1:]
            sample_id = a[1].strip()
            text = self.root.controller.getSampleInfo(table, sample_id)
            self.description.config(state=NORMAL)
            self.description.delete(1.0, END)
            self.description.insert(END, text)
            self.description.config(state=DISABLED)

    def drawPage(self):
        self.unclassified_listbox.grid(row=2,rowspan=1, column=1)
        self.unclassifiedLabel.grid(row=1, column=1)
        self.description.grid(row=4, columnspan=5, sticky=N+S+E+W)
        self.description.config(state=DISABLED)
        self.pack()
        self.current = None
        self.poll()

    def clearPage(self):
        self.pack_forget()

    def next(self):
        cursor = self.unclassified_listbox.curselection()
        raw = self.unclassified_listbox.get(int(cursor[0])).split('].')
        table = raw[0][1:]
        sample_name = raw[1]

        self.root.controller.addUnclassified(table, sample_name)
        return 'classify'

    def prev(self):
        return 'training'
        
class classificationPage(AHREAPage):
    def __init__(self, root):
        AHREAPage.__init__(self, root, 'classify')

    def drawPage(self):
        self.classify_label.grid(row=1, column=0, rowspan=4)
        self.dirac_button.grid(row=1, column=1)
        self.tsp_button.grid(row=2, column=1)
        self.tst_button.grid(row=3, column=1)
        self.ktsp_button.grid(row=4, column=1)
        self.adaptive_button.grid(row=5, column=1)
        self.pack()
    
    def setUpPage(self):
        s = self
        s.classify_label= Label(self, text="Please click a button for the algorithm you would like to classify against")
        s.dirac_button = Button(self, text="Classify using Dirac...", command=self.classifyDirac )
        s.tsp_button = Button(self, text="Classify using TSP...", command= self.classifyTSP )
        s.ktsp_button = Button(self, text="Classify using k-TSP...", command=self.classifyKTSP )
        s.tst_button = Button(self, text="Classify using TST...", command=self.classifyTST )
        s.adaptive_button = Button(self, text="Classify using Adaptive...", command=self.classifyAdaptive )
        
 
    def classifyDirac(self):
        if self.root.controller.dirac is not None:
            self.root.controller.classifyDirac()
            DiracClassificationResults(self)

    def classifyTSP(self):
        if self.root.controller.tsp is not None:
            self.root.controller.classifyTSP()
            TSPClassificationResults(self) 

    def classifyKTSP(self):
        if self.root.controller.ktsp is not None:
            self.root.controller.classifykTSP()
            KTSPClassificationResults(self)
        

    def classifyTST(self):
        if self.root.controller.tst is not None:
            self.root.controller.classifyTST()
            TSTClassificationResults(self)

    def classifyAdaptive(self):
        if self.root.controller.adaptive is not None:
            self.root.controller.classifyAdaptive()
            AdaptiveClassificationResults(self)

        
    def clearPage(self):
        self.pack_forget()

    def next(self):
        pass

    def prev(self):
        return 'addUnclassified'

    
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
