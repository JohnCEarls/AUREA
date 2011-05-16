from Tkinter import *
import tkFileDialog
import os
from AHREA.heuristic.LearnerQueue import LearnerQueue
class AHREAResults(Toplevel):
    def __init__(self,root):
        Toplevel.__init__(self)
        self.root = root
        self.position()

    def position(self):
        self.transient(self.root)
        self.geometry("+%d+%d" % (self.root.winfo_rootx()+50,
        self.root.winfo_rooty()+50))

    def saveResults(self, resultString):
        """
        Given a resultstring write the results out to file
        """
        options = {}
        options['defaultextension'] = '' # couldn't figure out how this works
        options['initialdir'] = 'data'
        options['initialfile'] = ''
        options['parent'] = self
        options['title'] = 'Save Results'
        filename = tkFileDialog.asksaveasfilename(**options)
        if filename:
            o = open(filename, 'w')
            o.write(resultString)
            o.close()

class DiracResults(AHREAResults):
    def __init__( self, root ):
        AHREAResults.__init__(self, root)
        self.title("AHREA: Dirac results")
        self.getData()
        self.displayTopNetworks()


    def getData(self):
        self.dirac = self.root.root.controller.dirac
        self.accuracy = self.root.root.controller.dirac_acc
        self.datapackage = self.root.root.controller.datapackage
        self.config = self.root.root.controller.config
        
        
    def displayTopNetworks(self):
        tn = self.dirac.getTopNetworks()
        resultString = ""
        resultString += "@acc: " + str(self.accuracy) + os.linesep
        num_net = self.config.getSetting("dirac","Number of Top Networks")[0]
        
        tn = tn[0:num_net]
        network_listbox = Listbox(self)
        for net in tn:
            network_listbox.insert(END, net)
            resultString += net + os.linesep
            
        network_listbox.pack()
        save_button = Button(self, text="Save...", command=lambda:self.saveResults(resultString))
        save_button.pack()

     
class TSPResults(AHREAResults):
    def __init__(self, root ):
        AHREAResults.__init__(self, root)
        self.root = root
        self.getData()
        self.displayData()
    
    def getData(self):
        self.tsp = self.root.root.controller.tsp
        self.datapackage = self.root.root.controller.datapackage
        self.config = self.root.root.controller.config
        self.accuracy = self.root.root.controller.tsp_acc

    def displayData(self):
        ms = self.tsp.getMaxScores()
        row = 1
        row_key = self.config.getSetting("tsp","Row Key(genes/probes)")[0]
        resultString = "" 
        resultString += "@acc: " + str(self.accuracy) + os.linesep
        for genes in ms:
            column = 0
            tab = ''
            for gene in genes:
                gene_name = self.datapackage.getGeneName(gene, row_key)
                resultString += tab + gene_name
                Label(self,text=gene_name).grid(row=row, column=column, padx=10 )
                tab = '\t'
                column += 1
            resultString += os.linesep
            row += 1
        save_button = Button(self, text="Save...", command=lambda:self.saveResults(resultString))
        save_button.grid(row=row, column=1, sticky=E)

 
class TSTResults(AHREAResults):
    def __init__(self, root):
        AHREAResults.__init__(self, root)
        self.getData()
        self.displayData()

    def getData(self):
        self.tst = self.root.root.controller.tst
        self.datapackage = self.root.root.controller.datapackage
        self.config = self.root.root.controller.config
        self.accuracy = self.root.root.controller.tst_acc

    def displayData(self):
        ms = self.tst.getMaxScores()
        row = 1
        row_key = self.config.getSetting("tst","Row Key(genes/probes)")[0]
        resultString = "" 
        resultString += "@acc: " + str(self.accuracy) + os.linesep
        for genes in ms:
            column = 0
            tab = ''
            for gene in genes:
                gene_name = self.datapackage.getGeneName(gene, row_key)
                resultString += tab + gene_name
                Label(self,text=gene_name).grid(row=row, column=column, padx=10 )
                tab = '\t'
                column += 1
            resultString += os.linesep
            row += 1
        save_button = Button(self, text="Save...", command=lambda:self.saveResults(resultString))
        save_button.grid(row=row, column=2, sticky=E)

 

class KTSPResults(AHREAResults):
    def __init__(self, root):
        AHREAResults.__init__(self, root)
        self.root = root
        self.getData()
        self.displayData()

    def getData(self):
        self.ktsp = self.root.root.controller.ktsp
        self.datapackage = self.root.root.controller.datapackage
        self.config = self.root.root.controller.config
        self.accuracy = self.root.root.controller.ktsp_acc

    def displayData(self):
        topk = self.ktsp.getMaxScores()
        row = 1
        row_key = self.config.getSetting("ktsp","Row Key(genes/probes)")[0]
        resultString = "" 
        resultString += "@acc: " + str(self.accuracy) + os.linesep
        for genes in topk:
            column = 0
            tab = ''
            for gene in genes:
                gene_name = self.datapackage.getGeneName(gene, row_key)
                resultString += tab + gene_name
                Label(self,text=gene_name).grid(row=row, column=column, padx=10 )
                tab = '\t'
                column += 1
            resultString += os.linesep
            row += 1
        save_button = Button(self, text="Save...", command=lambda:self.saveResults(resultString))
        save_button.grid(row=row, column=1, sticky=E)

class AdaptiveResults(AHREAResults):
    def __init__(self,root):
        AHREAResults.__init__(self, root)
        self.getData()
        self.buildDisplay()
       
    def getData(self):
        learnerMap = ['', '', '', '']
        learnerMap[LearnerQueue.dirac] = "DiRaC"
        learnerMap[LearnerQueue.tsp] = "TSP"
        learnerMap[LearnerQueue.tst] = "TST"
        learnerMap[LearnerQueue.ktsp] = "k-TSP"
        self.datapackage = self.root.root.controller.datapackage
        c = self.root.root.controller
        self.history = c.adaptive_history
        winner = c.adaptive_settings['learner']
        resultStr = "Top Learner : " + learnerMap[winner] + "@acc: " + str(c.adaptive_acc) + os.linesep
        resultStr += "="*30
        resultStr += os.linesep
        if winner == LearnerQueue.dirac:
            tn = c.adaptive.getTopNetworks()
            num_net = c.adaptive_settings['numTopNetworks']
            
            for net in tn:                
                resultStr += net + os.linesep
        else:
            l = c.adaptive.getMaxScores()
            row_key = c.adaptive_settings['data_type'] 
            for genes in l:
                column = 0
                tab = ''
                for gene in genes:
                    gene_name = self.datapackage.getGeneName(gene, row_key)
                    resultStr += tab + gene_name
                    tab = '\t'
                resultStr += os.linesep
        resultStr += c.adaptive_setting_string 
        self.resultString = resultStr
        #self.resultString gets displayed
        #resultStr (with history) gets Saved
        for acc, txt in self.history:
            resultStr += "@accuracy:"+str(acc) + os.linesep
            resultStr += txt
             
        self.save_button = Button(self, text="Save...", command=lambda:self.saveResults(resultStr))

    def buildDisplay(self):
        r = 0
        c = 0
        for row,line in enumerate(self.resultString.split(os.linesep)):
            r=row
            for col, val in enumerate(line.split('\t:')):
                if col > c:
                    c = col   
                Label(self, text=val).grid(column=col, row=row)
        self.save_button.grid(row=r, column=c, sticky=E)


class DiracClassificationResults(AHREAResults):
    def __init__(self, root):
        AHREAResults.__init__(self, root)
        self.getData()
        self.buildDisplay()

    def getData(self):
        self.dirac = self.root.root.controller.dirac
        self.dirac_results = self.root.root.controller.dirac_classification
        self.datapackage = self.root.root.controller.datapackage
        self.config = self.root.root.controller.config

    def buildDisplay(self):
        c1_name =self.root.root.controller.class1name
        c2_name = self.root.root.controller.class2name

        if self.dirac_results == 0:
            className = c1_name
        else:
            className = c2_name
        self.result = Label(self, text = "classifies as " + className)

        self.result.pack()    
 
class TSPClassificationResults(AHREAResults):
    def __init__(self, root):
        AHREAResults.__init__(self, root)
        self.getData()
        self.buildDisplay()

    def getData(self):
        self.tsp = self.root.root.controller.tsp
        self.tsp_results = self.root.root.controller.tsp_classification
        self.datapackage = self.root.root.controller.datapackage

    def buildDisplay(self):
        c1_name =self.root.root.controller.class1name
        c2_name = self.root.root.controller.class2name

        if self.tsp_results == 0: 
            className = c1_name
        else:
            className = c2_name
        self.result = Label(self, text = "classifies as " + className)

        self.result.pack()

class TSTClassificationResults(AHREAResults):
    def __init__(self, root):
        AHREAResults.__init__(self, root)
        self.getData()
        self.buildDisplay()

    def getData(self):
        self.tst = self.root.root.controller.tst
        self.tst_results = self.root.root.controller.tst_classification
        self.datapackage = self.root.root.controller.datapackage

    def buildDisplay(self):
        c1_name =self.root.root.controller.class1name
        c2_name = self.root.root.controller.class2name

        if self.tst_results == 0: 
            className = c1_name
        else:
            className = c2_name
        self.result = Label(self, text = "classifies as " + className)

        self.result.pack()

class KTSPClassificationResults(AHREAResults):
    def __init__(self, root):
        AHREAResults.__init__(self, root)
        self.getData()
        self.buildDisplay()

    def getData(self):
        self.ktsp = self.root.root.controller.ktsp
        self.ktsp_results = self.root.root.controller.ktsp_classification
        self.datapackage = self.root.root.controller.datapackage

    def buildDisplay(self):
        c1_name =self.root.root.controller.class1name
        c2_name = self.root.root.controller.class2name

        if self.ktsp_results == 0: 
            className = c1_name
        else:
            className = c2_name
        self.result = Label(self, text = "classifies as " + className)

        self.result.pack()

class AdaptiveClassificationResults(AHREAResults):
    def __init__(self, root):
        AHREAResults.__init__(self, root)
        self.getData()
        self.buildDisplay()

    def getData(self):
        self.adaptive = self.root.root.controller.adaptive
        self.adaptive_results = self.root.root.controller.adaptive_classification
        self.datapackage = self.root.root.controller.datapackage

    def buildDisplay(self):
        c1_name =self.root.root.controller.class1name
        c2_name = self.root.root.controller.class2name

        if self.adaptive_results == 0:
            className = c1_name
        else:
            className = c2_name
        self.result = Label(self, text = "classifies as " + className)

        self.result.pack()
