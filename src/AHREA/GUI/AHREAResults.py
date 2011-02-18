from Tkinter import *

class DiracResults(Toplevel):
    def __init__( self, root ):
        Toplevel.__init__(self)
        self.title("AHREA: Dirac results")
        self.root = root
        self.getData()
        self.displayTopNetworks()


    def getData(self):
        self.dirac = self.root.root.controller.dirac
        self.datapackage = self.root.root.controller.datapackage
        self.config = self.root.root.controller.config
        
    def displayTopNetworks(self):
        tn = [self.datapackage.getGeneNetName(gn) for gn in self.dirac.getTopNetworks()]
        num_net = self.config.getSetting("dirac","Number of Top Networks")[0]
        tn = tn[0:num_net]
        network_listbox = Listbox(self)
        for net in tn:
            network_listbox.insert(END, net)
        network_listbox.pack()
     
class TSPResults(Toplevel):
    def __init__(self, root ):
        Toplevel.__init__(self)
        self.root = root
        self.getData()
        self.displayData()
    
    def getData(self):
        self.tsp = self.root.root.controller.tsp
        self.datapackage = self.root.root.controller.datapackage
        self.config = self.root.root.controller.config

    def displayData(self):
        ms = self.tsp.getMaxScores()
        row = 1
        row_key = self.config.getSetting("tsp","Row Key(genes/probes)")[0]
        for genes in ms:
            column = 0
            for gene in genes:
                gene_name = self.datapackage.getGeneName(gene, row_key)
                Label(self,text=gene_name).grid(row=row,column=column )
                column += 1
            row += 1

 
class TSTResults(Toplevel):
    def __init__(self, root):
        Toplevel.__init__(self)
        self.root = root
        self.getData()
        self.displayData()

    def getData(self):
        self.tst = self.root.root.controller.tst
        self.datapackage = self.root.root.controller.datapackage
        self.config = self.root.root.controller.config
 
    def displayData(self):
        ms = self.tst.getMaxScores()
        row = 1
        row_key = self.config.getSetting("tst","Row Key(genes/probes)")[0]
        for genes in ms:
            column = 0
            for gene in genes:
                gene_name = self.datapackage.getGeneName(gene, row_key)
                Label(self,text=gene_name).grid(row=row,column=column )

                column += 1
            row += 1

 

class KTSPResults(Toplevel):
    def __init__(self, root):
        Toplevel.__init__(self)
        self.root = root
        self.getData()
        self.displayData()

    def getData(self):
        self.ktsp = self.root.root.controller.ktsp
        self.datapackage = self.root.root.controller.datapackage
        self.config = self.root.root.controller.config
 
    def displayData(self):
        topk = self.ktsp.getMaxScores()
        row = 1
        row_key = self.config.getSetting("ktsp","Row Key(genes/probes)")[0]
          
        for genes in topk:        
            column = 0
            for gene in genes:
                gene_name = self.datapackage.getGeneName(gene, row_key)
                Label(self,text=gene_name).grid(row=row,column=column )

                column += 1
            row += 1

class DiracClassificationResults(Toplevel):
    def __init__(self, root):
        Toplevel.__init__(self)
        self.root = root
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
 
class TSPClassificationResults(Toplevel):
    def __init__(self, root):
        Toplevel.__init__(self)
        self.root = root
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

class TSTClassificationResults(Toplevel):
    def __init__(self, root):
        Toplevel.__init__(self)
        self.root = root
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

class KTSPClassificationResults(Toplevel):
    def __init__(self, root):
        Toplevel.__init__(self)
        self.root = root
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

class AdaptiveClassificationResults(Toplevel):
    def __init__(self, root):
        Toplevel.__init__(self)
        self.root = root
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
