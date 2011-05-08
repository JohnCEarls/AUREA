from AHREA.learner import ktsp, tst, dirac, tsp
from AHREA.heuristic.LearnerQueue import LearnerQueue 
from AHREA.heuristic.Adaptive import Adaptive
from AHREA.parser.SOFTParser import *
from AHREA.parser.CSVParser import *
from AHREA.parser.GMTParser import *
from AHREA.parser.SettingsParser import *
from AHREA.packager.DataCleaner import *
from AHREA.packager.DataPackager import *
from AHREA.GUI.AHREAPage import InputError
from AHREA.GUI.AHREAApp import AHREARemote

from Tkinter import *
import time
import os
import shutil

class AHREAController:
    def __init__(self, workspace ):
        """
        This is the controller (MVC design pattern) for the GUI.
        workspace is the folder that contains the config file and where
        temporary files and data files will be brought.
        """
        self.softFile = []
        self.geneNetworkFile = None
        self.geneSynonymFile = None
        self.softparser = []
        self.datatable = []
        self.datapackage = None
        self.workspace = workspace
        configFile = os.path.join(self.workspace, 'data', 'config.xml')
        logo = os.path.join(self.workspace, 'data', 'AHREA-logo.pgm')
        if not os.path.exists(configFile):
            raise Exception, configFile + " not found.  Exiting"
        if not os.path.exists(logo):
            raise Exception, logo + " not found.  Exiting"
 
        self.config = SettingsParser(configFile)
        self.dirac = None
        self.tsp = None
        self.ktsp = None
        self.tst = None
        self.adaptive = None
        self.dependency_state = [0 for x in range(AHREARemote.NumStates)]#see AHREAApp.AHREARemote for mappings

    def setSOFTFile(self, softFile):
        raise Exception, "controller.setSOFTFile deprecated"
        self.softFile = softFile

    def addSOFTFile(self, softFile):   
        self.softFile.append( softFile ) 

    def setGeneNetworkFile(self, gnFile):
        self.geneNetworkFile = gnFile

    def setSynonymFile(self, sFile):
        self.geneSynonymFile = sFile

    def getNetworkInfo(self):
        if self.datapackage is not None:
            fname = self.geneNetworkFile
            gnc = self.datapackage.getGeneNetCount()
            if gnc is None:
                return None
            count, ave, max, min = gnc
            return (fname, count, ave, max, min)
        else:
            return None

    def setApp(self, app):
        self.app = app
        self.remote = app.remote

    def updateState(self, dependency, satisfied):
        """
        Given a dependency, update to satisfied in global dependencies, propagating change
        """
        #update provided state
        self.dependency_state[dependency] = satisfied
        #clear all dependents
        for i,d in enumerate(self.remote.getDependents(dependency)):
            if d == 1:
                self.updateState(i, 0)
        self.remote.stateChange()

    def initWorkspace(self):
        """
        Initialize the workspace files.
        Copy from the system any necessary files. (config, gene_syn, etc)
        DEPRECATED!!!!
        """
        raise Exception, "initWorkspace is deprecated, download the workspace.zip file"

    def downloadSOFT(self, softfilename):
        self.app.status.clear()
        self.app.status.set("Downloading " + softfilename)
        dl = SOFTDownloader(softfilename, output_directory=self.config.getSetting("datatable", "Data Folder")[0])
        self.app.status.clear()
        return dl.getFilePath()

    def loadFiles(self):
        """
        Loads all of the specified files
        """
        self.app.status.clear()
        self.parseSOFTFiles()
        self.buildDataTables()
        self.buildDataPackage() 
        if self.geneNetworkFile:
            self.parseNetworkFile()
        if self.geneSynonymFile:
            self.app.status.set("Loading Synonyms")
            self.datapackage.addSynonyms(self.geneSynonymFile) 
        self.app.status.clear()
        self.app.status.set("Data import complete")
    
    def unloadFiles(self):
        self.app.status.clear()
        self.softparser = []
        self.geneNetworkParser = None
        self.datapackage = None
        self.datatable = []
        self.softFile = []

    def parseSOFTFiles(self):
        """
        adds SOFTparser objects to softparser
        """
        for file in self.softFile:
            self.app.status.set("Parsing " + file)
            if file[-3:] == "csv":
                self.tmpfile = file
                self._done = False
                def addCSV():
                    self.softparser.append(CSVParser(self.tmpfile, probe_column_name=self.tmp_probe_column.get(), gene_column_name=self.tmp_gene_column.get() ))
                    self.d.destroy()
                    
                self.d = dialog = Toplevel(self.app)
                dialog.protocol('WM_DELETE_window', dialog.destroy)
                Label(dialog, text="Enter settings for " + file).grid(row=0, column=0, columnspan=2)
                
                Label(dialog, text="Probe Column:").grid(row=1, column=0)
                self.tmp_probe_column=StringVar()
                Entry(dialog, textvariable=self.tmp_probe_column).grid(row=1, column=1)
                Label(dialog, text="Gene Column:").grid(row=2, column=0)
                self.tmp_gene_column=StringVar()
                Entry(dialog, textvariable=self.tmp_gene_column).grid(row=2, column=1)
                Button(dialog, text="OK", command=addCSV).grid(row=3)
                self.app.wait_window(dialog)
                    
                #self.softparser.append(CSVParser(file,probe_column=probe_column.get(), gene_column=gene_column.get() ))
            else:
                self.softparser.append(SOFTParser(file))
            self.app.status.clear()

    def buildDataTables(self):
        """
        Builds a table for each data file
        """
        self.app.status.set("Building tables")
        collision = self.config.getSetting("datatable", "Gene Collision Rule")[0]
        bad_data =self.config.getSetting("datatable", "Bad Data Value")[0] 
        gene_column = self.config.getSetting("datatable", "Gene Column")[0]
        probe_column = self.config.getSetting("datatable", "Probe Column")[0]
        for sf in self.softparser:
            if isinstance(sf, SOFTParser):
                self.datatable.append( DataTable(probe_column, gene_column, collision, bad_data))
                self.datatable[-1].getSOFTData(sf)
            else:
                self.datatable.append( DataTable(probe_column, gene_column, collision, bad_data))      
                self.datatable[-1].getCSVData(sf)

    def buildDataPackage(self):
        """
        Merges all the data tables into one package from which we pull our
        data for learning
        """
        self.app.status.set("Building data package")
        self.datapackage = dataPackager()
        for dt in self.datatable:
            self.datapackage.addDataTable(dt)
        self.datapackage.mergeTables()
        self.app.status.clear()

    def getDataPackagingResults(self):
        """
        Returns a list of tuples with
        (genes in merge, probes in merge)
        """
        if self.datapackage is not None:
            return self.datapackage.getDataCount()
        else:
            return (None,None)

    def getLearnerAccuracy(self):
        """
        Returns the apparent accuracy of the learners over the training set
        (TSP,kTSP,TST,DiRaC, Adaptive)
        """
        #TODO
        return (None,None,None,None,None)

    def getCrossValidationResults(self):
        """
        Returns the cross validation accuracy of the learners over 
        the training set
        (TSP,kTSP,TST,DiRaC, Adaptive)
        """
        #TODO
        return (None,None,None,None,None)


    def parseNetworkFile(self):
        """
        Parse network file and add networks to datapackage
        """    
        self.app.status.set("Parsing network file")
        self.geneNetworkParser = GMTParser(self.geneNetworkFile)
        self.app.status.set("Loading gene networks")
        self.datapackage.addGeneNetwork(self.geneNetworkParser.getAllNetworks())
        self.app.status.clear()
    
    def createClassification(self, page):
        """
        Gets and sets the class labels
        """
        self.datapackage.clearClassification()
        c1 = self.class1name = page.className1.get().strip()
        c2 = self.class2name = page.className2.get().strip()
        self.datapackage.createClassification(c1)
        self.datapackage.createClassification(c2)

    def getClassificationInfo(self):
        """
        Returns the names and sizes of the partitioned classes 
        (c1name, c1size, c2name, c2size)
        None is returned if classifications have not been created
        """
        if self.datapackage is not None:
            classinfo = self.datapackage.getClassifications()
            if len(classinfo) > 0:
                return (classinfo[0][0], len(classinfo[0][1]), classinfo[1][0], len(classinfo[1][1]))
        return ('',0,'',0)

    def partitionClasses(self, class1List, class2List):
        """
        Puts the samples into their chosen classes
        """
        self.datapackage.clearClassSamples()
        for table, sample in class1List:
            self.datapackage.addToClassification(self.class1name, table, sample)

        for table, sample in class2List:
            self.datapackage.addToClassification(self.class2name, table, sample)

    def getSamples(self):
        """
        Returns a list of strings describing all available samples in the data tables
        [ '[dt1].samp_name', '[dt2].samp_name', ...]
        """
        sample_list = []
        for table in self.datapackage.getTables():
            table_id = table.dt_id
            for sample_id in table.getSamples():
                text = "[" + table_id + "]." + sample_id
                sample_list.append(text)
        return sample_list

    def clearClassSamples(self):
        """
        Removes samples from any classifications
        """
        self.datapackage.clearClassSamples()
   
    def getUntrainedSamples(self):
        """
        This is basically getSamples with the training set removed
        """
        currentClassifications = self.datapackage.getClassifications()
        classified_samples = []
        for cc_class, cc_samples in currentClassifications:
            for samp in cc_samples:
                 text = "[" + samp[0] + "]." + samp[1]
                 classified_samples.append(text)
        all_samples = self.getSamples()
        #do an inorder comparison to build list
        classified_samples.sort()
        all_samples.sort()
        unclassified_samples = []
        curr_class_samp_i = 0
        
        for sample in all_samples:
            if curr_class_samp_i == len(classified_samples) or sample != classified_samples[curr_class_samp_i]:
                unclassified_samples.append(sample)
            else:
                curr_class_samp_i += 1
        return unclassified_samples        

        
    def addUnclassified(self, table, sample_name):
        """
        Adds an unclassified sample to the data package
        """
        self.datapackage.setUnclassified(table, sample_name)
        
         
    def getSampleInfo(self, table, sample_id):
        """
        Gets the information about a sample if it is available
        """
        table = self.datapackage.getTable(table)        
        return table.getSampleDescription(sample_id)
 
    def trainDirac(self):
        self.app.status.clear()
        self.app.status.set("Preparing Dirac")
        min_net = self.config.getSetting("dirac","Minimum Network Size")[0]
        row_key = self.config.getSetting("dirac","Row Key(genes/probes)")[0]
        data_vector, num_genes = self.datapackage.getDataVector(row_key)
        class_vector = self.datapackage.getClassVector()
        gene_net, gene_net_size = self.datapackage.getGeneNetVector(min_net)
        self.app.status.set("Training Dirac")
        self.dirac = dirac.Dirac(data_vector, num_genes,class_vector, gene_net, gene_net_size)
        self.dirac.train()
        self.app.status.set("Training Complete")

    def trainTSP(self):
        """
        Performs the training of TSP
        """
        self.app.status.set("Preparing TSP")
        filters = self.config.getSetting("tsp","filters")
        row_key = self.config.getSetting("tsp","Row Key(genes/probes)")[0]
         
        data_vector, num_genes = self.datapackage.getDataVector(row_key)
        class_vector = self.datapackage.getClassVector()
        vecFilter = tsp.IntVector()
        for val in filters:
            vecFilter.push_back(val)
        self.app.status.set("Training TSP")
        self.tsp = tsp.TSP(data_vector, num_genes, class_vector, vecFilter)
        self.tsp.train()
        self.app.status.set("Training Complete")

    def trainTST(self):
        """
        Performs the training of tst
        """
        self.app.status.set("Preparing TST")
        filters = self.config.getSetting("tst","filters")
        row_key = self.config.getSetting("tst","Row Key(genes/probes)")[0]
         
        data_vector, num_genes = self.datapackage.getDataVector(row_key)
        class_vector = self.datapackage.getClassVector()
        vecFilter = tst.IntVector()
        for val in filters:
            vecFilter.push_back(val)
        self.app.status.set("Training TST")
        self.tst = tst.TST(data_vector, num_genes, class_vector, vecFilter)    
        self.tst.train()
        self.app.status.set("Training Complete")

    def trainkTSP(self):
        """
        Performs the training of k-TSP
        """
        self.app.status.set("Preparing k-TSP")
        maxk = self.config.getSetting("ktsp","Maximum K value")[0]
        cross_remove = self.config.getSetting("ktsp","Remove for Cross Validation")[0]
        num_cross = self.config.getSetting("ktsp","Number of Cross Validation Runs")[0]
        row_key = self.config.getSetting("ktsp","Row Key(genes/probes)")[0]
        data_vector, num_genes = self.datapackage.getDataVector(row_key)
        filters = self.config.getSetting("ktsp","filters")
        class_vector = self.datapackage.getClassVector()
        vecFilter = tst.IntVector()
        for x in filters:
            if x < 2*maxk:
                raise Exception("Ktsp setting error.  The filters must be at least twice the Maximum K value")
            vecFilter.push_back(x)

        self.app.status.set("Training k-TSP(this could take a while, get a Coke)")
        self.ktsp = ktsp.KTSP( data_vector, num_genes, class_vector, vecFilter, maxk, cross_remove, num_cross)
        self.ktsp.train()
        self.app.status.set("Training Complete")

    def trainAdaptive(self, target_accuracy, maxTime  ):
        self.app.status.set("Configuring adaptive training")
        
        try:
            acc = float(target_accuracy)
        except Exception:
            acc = .9
        if acc > 1.0 or acc <= .0:
            acc = .9
        try:
            mtime = int(maxTime)
        except:
            mtime = 2**20
     
        maxTime = mtime
        target_accuracy = acc
        #build learner queue
        self._adaptiveSetup()
        #create adaptive object
        adaptive = Adaptive(self.learnerqueue, app_status_bar = self.app.status)
        top_acc, top_settings, top_learner = adaptive.getLearner(target_accuracy, maxTime)
        #store adaptive results
        self.adaptive = top_learner
        self.adaptive_settings = top_settings


    def _adaptiveSetup(self):
        self._adaptiveSetupLearnerQueue()
        self.app.status.set("Configuring dirac")
        self._adaptiveSetupDirac()
        self.app.status.set("Configuring tsp")
        self._adaptiveSetupTSP()
        self.app.status.set("Configuring tst")
        self._adaptiveSetupTST()
        self.app.status.set("Configuring ktsp")
        self._adaptiveSetupKTSP()


    def _adaptiveSetupLearnerQueue(self):
        dp = self.datapackage
        #Learner Queue Settings
        wilc_data_type = self.config.getSetting("adaptive", "Wilcoxon Row Key (gene/probe)")[0]
        weight = self.config.getSetting("adaptive", "Initial Weight (dirac,tsp,tst,ktsp)")
        scale = None#self.config.getSetting("adaptive", "Initial Scale (dirac,tsp,tst,ktsp)")
        min_weight = self.config.getSetting("adaptive", "Minimum Weight")[0]
      
        self.learnerqueue = LearnerQueue(dp, wilc_data_type, weight, scale, min_weight)
    

    def _adaptiveSetupDirac(self):
        #dirac settings
        d_row_key = self.config.getSetting("adaptive", "Dirac-Row Key(gene/probe)")[0]
        d_min_net = self.config.getSetting("adaptive", "Dirac-Min. Network Size Range")
        d_num_top_net = self.config.getSetting("adaptive", "Dirac-Num Top Networks Range")
        self.learnerqueue.genDirac(d_min_net, d_num_top_net, d_row_key)        

    def _adaptiveSetupTSP(self):
        #tsp settings
        p_row_key = self.config.getSetting("adaptive", "TSP-Row Key(gene/probe)")[0]
        p_equijoin = self.config.getSetting("adaptive", "TSP-Only use equal filters")[0]
        p_filter_1 = self.config.getSetting("adaptive", "TSP-Filter 1 Range")
        p_filter_2 = self.config.getSetting("adaptive", "TSP-Filter 2 Range")
        self.learnerqueue.genTSP(tuple(p_filter_1), tuple(p_filter_2), p_equijoin, p_row_key)

    def _adaptiveSetupTST(self):
        #tst settings
        t_row_key = self.config.getSetting("adaptive", "TST-Row Key(gene/probe)")[0]
        t_equijoin = self.config.getSetting("adaptive", "TST-Only use equal filters")[0]
        t_filter_1 = self.config.getSetting("adaptive", "TST-Filter 1 Range")
        t_filter_2 = self.config.getSetting("adaptive", "TST-Filter 2 Range")
        t_filter_3 = self.config.getSetting("adaptive", "TST-Filter 3 Range")           
        self.learnerqueue.genTST(tuple(t_filter_1), tuple(t_filter_2), tuple(t_filter_3), t_equijoin, t_row_key)

    def _adaptiveSetupKTSP(self):
        #ktsp settings
        k_row_key = self.config.getSetting("adaptive", "k-TSP-Row Key(gene/probe)")[0]
        k_equijoin = self.config.getSetting("adaptive", "k-TSP-Only use equal filters")[0]
        k_filter_1 = self.config.getSetting("adaptive", "k-TSP-Filter 1 Range")
        k_filter_2 = self.config.getSetting("adaptive", "k-TSP-Filter 2 Range")
        k_maxK = self.config.getSetting("adaptive", "Maximum k Range")
        k_ncv = self.config.getSetting("adaptive", "Number of Internal CV to find k Range")
        k_nlo = self.config.getSetting("adaptive", "Number to leave out on Internal CV to find k Range")
        self.learnerqueue.genKTSP(tuple(k_maxK),tuple(k_ncv), tuple(k_nlo), tuple(k_filter_1), tuple(k_filter_2), k_equijoin, k_row_key)
 
       

    def classifyDirac(self):
        dp = self.datapackage
        num_net = self.config.getSetting("dirac","Number of Top Networks")[0]
        row_key = self.config.getSetting("dirac","Row Key(genes/probes)")[0]
        self._checkRowKey(row_key)
        self.dirac.addUnclassified(dp.getUnclassifiedDataVector(row_key ))
        self.dirac_classification = self.dirac.classify(num_net)

    def classifyTSP(self):
        dp = self.datapackage
        row_key = self.config.getSetting("tsp","Row Key(genes/probes)")[0]
        self._checkRowKey(row_key)
        self.tsp.addUnclassified(dp.getUnclassifiedDataVector(row_key))
        self.tsp_classification = self.tsp.classify()

    def classifyTST(self):
        dp = self.datapackage
        row_key = self.config.getSetting("tst","Row Key(genes/probes)")[0]
        self._checkRowKey(row_key)
        self.tst.addUnclassified(dp.getUnclassifiedDataVector(row_key))
        self.tst_classification = self.tst.classify()

    def classifykTSP(self):
        dp = self.datapackage
        row_key = self.config.getSetting("ktsp","Row Key(genes/probes)")[0]
        self._checkRowKey(row_key)
        self.ktsp.addUnclassified(dp.getUnclassifiedDataVector(row_key))
        self.ktsp_classification = self.ktsp.classify()

    def classifyAdaptive(self):
        dp = self.datapackage
        learner = self.adaptive
        settings = self.adaptive_settings
        row_key = settings['data_type']
        learner.addUnclassified(dp.getUnclassifiedDataVector(row_key))
        
        if settings['learner'] == LearnerQueue.dirac:
            num_net =settings['numTopNetworks']
            self.adaptive_classification = learner.classify(num_net)
        else:
            self.adaptive_classification = learner.classify()
       
    def _checkRowKey(self, row_key, srcStr="Not Given"):
        if row_key not in ['gene', 'probe']:
            raise InputError(srcStr, "Given key " + row_key + " is invalid" )
