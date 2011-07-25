from AUREA.learner import ktsp, tst, dirac, tsp
from AUREA.heuristic.LearnerQueue import LearnerQueue 
from AUREA.heuristic.Adaptive import Adaptive
from AUREA.parser.SOFTParser import *
from AUREA.parser.CSVParser import *
from AUREA.parser.GMTParser import *
from AUREA.parser.SettingsParser import *
from AUREA.packager.DataCleaner import *
from AUREA.packager.DataPackager import *
from AUREA.GUI.Page import InputError
from AUREA.GUI.App import AUREARemote

from Tkinter import *
import time
import os
import shutil
#thread_message_queue
class Controller:
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
        logo = os.path.join(self.workspace, 'data', 'AUREA-logo-200.pgm')
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

        self.tsp_acc = None
        self.ktsp_acc = None
        self.tst_acc = None
        self.dirac_acc = None
        self.adaptive_acc_tuple = None

        #for classification page
        self.tsp_classified_results = []
        self.ktsp_classified_results = []
        self.tst_classified_results = []
        self.dirac_classified_results = []
        self.adaptive_classified_results = []

        self.tsp_cv = None
        self.ktsp_cv = None
        self.tst_cv = None
        self.dirac_cv = None
        self.adaptive_cv = None

       

        self.dependency_state = [0 for x in range(AUREARemote.NumStates)]#see App.AUREARemote for mappings

    def setSOFTFile(self, softFile):
        """
        DEPRECATED  
        """
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
        self.queue = self.app.thread_message_queue

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
        """
        Note raises urllib2.URLError when the download attempt fails
        """
        self.queue.put(('statusbarclear',None))
        self.queue.put(('statusbarset',"Downloading " + softfilename))
        dl = SOFTDownloader(softfilename, output_directory=self.config.getSetting("datatable", "Data Folder")[0])
        self.queue.put(('statusbarclear',None))
        return dl.getFilePath()

    def loadFiles(self):
        """
        Loads all of the specified files
        """
        self.queue.put(('statusbarclear',None))
        self.parseSOFTFiles()
        self.buildDataTables()
        self.buildDataPackage() 
        if self.geneNetworkFile:
            self.parseNetworkFile()
        if self.geneSynonymFile:
            self.queue.put(('statusbarset',"Loading Synonyms"))
            self.datapackage.addSynonyms(self.geneSynonymFile) 
        self.queue.put(('statusbarclear',None))
        self.queue.put(('statusbarset',"Data import complete"))
    
    def unloadFiles(self):
        self.queue.put(('statusbarclear',None))
        self.softparser = []
        self.geneNetworkParser = None
        self.datapackage = None
        self.datatable = []
        self.softFile = []
        self.clearLearningAlg()

    def parseSOFTFiles(self):
        """
        adds SOFTparser objects to softparser
        """
        for file in self.softFile:
            self.queue.put(('statusbarset',"Parsing " + file))
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
            self.queue.put(('statusbarclear',None))

    def buildDataTables(self):
        """
        Builds a table for each data file
        """
        self.queue.put(('statusbarset',"Building tables"))
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
        self.queue.put(('statusbarset',"Building data package"))
        self.datapackage = dataPackager()
        for dt in self.datatable:
            self.datapackage.addDataTable(dt)
        self.datapackage.mergeTables()
        self.queue.put(('statusbarclear',None))

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
        
        return (self.tsp_acc, self.ktsp_acc,self.tst_acc,self.dirac_acc,self.adaptive_acc_tuple)

    def getCrossValidationResults(self):
        """
        Returns the cross validation accuracy of the learners over 
        the training set
        (TSP,kTSP,TST,DiRaC, Adaptive)
        """
        #TODO
        return (self.tsp_cv,self.ktsp_cv,self.tst_cv,self.dirac_cv,self.adaptive_cv)


    def parseNetworkFile(self):
        """
        Parse network file and add networks to datapackage
        """    
        self.queue.put(('statusbarset',"Parsing network file"))
        self.geneNetworkParser = GMTParser(self.geneNetworkFile)
        self.queue.put(('statusbarset',"Loading gene networks"))
        self.datapackage.addGeneNetwork(self.geneNetworkParser.getAllNetworks())
        self.queue.put(('statusbarclear',None))
    
    def createClassification(self, page):
        """
        Gets and sets the class labels
        """
        self.clearLearningAlg()
        self.datapackage.clearClassification()
        c1 = self.class1name = page.className1.get().strip()
        c2 = self.class2name = page.className2.get().strip()
        self.datapackage.createClassification(c1)
        self.datapackage.createClassification(c2)

    def getClassificationInfo(self):
        """
        Returns the names and sizes of the partitioned classes 
        (c1name, c1size, c2name, c2size)
        ('',0,'',0) is returned if classifications have not been created
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
                sample_list.append(self._makeSampleString(table_id, sample_id))
        return sample_list
    
    def _makeSampleString(self, table_id, sample_id):
        """
        helper to keep sample strings consistent
        """
        return "[" + table_id + "]." + sample_id

    def getSubsets(self):
        """
        Returns a list of 2-tuples, 
        [
        (description, list of sample names formatted to match getSamples),
        ...]
        
        """
        sample_list = self.getSamples()[:]
        sample_set = set(self.getSamples())
        subset_list = []        
        

        for table in self.datapackage.getTables():
            table_id = table.dt_id
            for ssetdesc, ssetsamples in table.subsets:
                sschecked_list = []
                for sample_id in ssetsamples:
                    sssid = self._makeSampleString(table_id, sample_id)
                    if sssid in sample_set:
                        sschecked_list.append(sssid)
                subset_list.append((ssetdesc, sschecked_list))

        return subset_list
 

    def clearClassSamples(self):
        """
        Removes samples from any classifications
        """
        if self.datapackage is not None:
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
 
    def _getLearnerAccuracy(self, learner, row_key):
        """
        Takes a trained learner (and its row_key gene/probe)
         and returns the results of
        classifying the Trained Data
        Returns a tuple (T0,F0, T1, F1, MCC)
        Note T0 = True Positive = True class 1
        """
        import math
        def MCC(TP,FP, TN, FN):
            den = math.sqrt(float((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)))
            if den < .000001:
                #http://en.wikipedia.org/wiki/Matthews_correlation_coefficient
                den = 1.0
            return float(TP*TN - FP*FN)/den
        dp = self.datapackage
        class1, class2 = dp.getClassifications()
        T0 = 0
        F0 = 0
        T1 = 0
        F1 = 0
        for table, sample in class1[1]:
            dp.clearUnclassified()
            self.addUnclassified(table, sample)
            learner.addUnclassified(dp.getUnclassifiedDataVector(row_key))
            if learner.classify() == 0:
                T0 += 1
            else:
                F1 += 1  

        for table, sample in class2[1]:
            dp.clearUnclassified()
            self.addUnclassified(table, sample)
            learner.addUnclassified(dp.getUnclassifiedDataVector(row_key))
            if learner.classify() == 1:
                T1 += 1
            else:
                F0 += 1  
        dp.clearUnclassified()
        
        return (T0,F0, T1, F1, MCC(T0,F0, T1,F1))



    def trainDirac(self, crossValidate=False):
        self.queue.put(('statusbarclear',None))
        self.queue.put(('statusbarset',"Preparing Dirac"))
        min_net = self.config.getSetting("dirac","Minimum Network Size")[0]
        row_key = self.config.getSetting("dirac","Row Key(genes/probes)")[0]
        numTopNetworks = self.config.getSetting("dirac","Number of Top Networks")[0]
        data_vector, num_genes = self.datapackage.getDataVector(row_key)
        class_vector = self.datapackage.getClassVector()

        gene_net, gene_net_size = self.datapackage.getGeneNetVector(min_net)
        netMap = self.datapackage.gene_net_map
        d = dirac.Dirac(data_vector, num_genes,class_vector, gene_net, gene_net_size, numTopNetworks, netMap)
        if crossValidate:
            return d
        
        self.queue.put(('statusbarset',"Training Dirac"))
        d.train()
        self.dirac = d
        self.queue.put(('statusbarset',"Training Complete, Checking Accuracy"))
        self.dirac_acc = self._getLearnerAccuracy(self.dirac, row_key)
        self.queue.put(('statusbarset',"Accuracy Check Complete"))
    

    def trainTSP(self, crossValidate=False):
        """
        Performs the training of TSP
        """
        self.queue.put(('statusbarset',"Preparing TSP"))
        filters = self.config.getSetting("tsp","filters")
        row_key = self.config.getSetting("tsp","Row Key(genes/probes)")[0]
         
        data_vector, num_genes = self.datapackage.getDataVector(row_key)
        class_vector = self.datapackage.getClassVector()
        vecFilter = tsp.IntVector()
        for val in filters:
            vecFilter.push_back(val)
        self.queue.put(('statusbarset',"Init TSP"))

        t = tsp.TSP(data_vector, num_genes, class_vector, vecFilter)
        if crossValidate:
            return t
        self.queue.put(('statusbarset',"Training TSP"))
        self.tsp = t
        t.train()
        self.queue.put(('statusbarset',"Training Complete, Checking Accuracy"))
        self.tsp_acc = self._getLearnerAccuracy(self.tsp, row_key)
        self.queue.put(('statusbarset',"Accuracy Check Complete"))


    def trainTST(self, crossValidate=False):
        """
        Performs the training of tst
        """
        self.queue.put(('statusbarset',"Preparing TST"))
        filters = self.config.getSetting("tst","filters")
        row_key = self.config.getSetting("tst","Row Key(genes/probes)")[0]
         
        data_vector, num_genes = self.datapackage.getDataVector(row_key)
        class_vector = self.datapackage.getClassVector()
        vecFilter = tst.IntVector()
        for val in filters:
            vecFilter.push_back(val)
        t = tst.TST(data_vector, num_genes, class_vector, vecFilter)    
        if crossValidate:
            return t
        self.tst = t
        self.queue.put(('statusbarset',"Training TST"))
        t.train()
        self.queue.put(('statusbarset',"Training Complete, Checking Accuracy"))
        self.tst_acc = self._getLearnerAccuracy(self.tst, row_key)
        self.queue.put(('statusbarset',"Accuracy Check Complete"))


    def trainkTSP(self, crossValidate=False):
        """
        Performs the training of k-TSP
        """
        self.queue.put(('statusbarset',"Preparing k-TSP"))
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

        
        k = ktsp.KTSP( data_vector, num_genes, class_vector, vecFilter, maxk, cross_remove, num_cross)
        if crossValidate:
            return k
        self.queue.put(('statusbarset',"Training k-TSP"))
        k.train()
        self.ktsp = k
        self.queue.put(('statusbarset',"Training Complete, Checking Accuracy"))
        
        self.ktsp_acc = self._getLearnerAccuracy(self.ktsp, row_key)
        self.queue.put(('statusbarset',"Accuracy Check Complete"))


    def trainAdaptive(self, target_accuracy, maxTime  ):
        self.queue.put(('statusbarset',"Configuring adaptive training"))
        
        acc = float(target_accuracy)
        mtime = int(maxTime)
        maxTime = mtime

        target_accuracy = acc
        #build learner queue
        self._adaptiveSetup()
        #create adaptive object
        adaptive = Adaptive(self.learnerqueue, app_status_bar = self.queue)
        top_acc, top_settings, top_learner = adaptive.getLearner(target_accuracy, maxTime)
        #store adaptive results (really should be in adaptive)
        self.adaptive_history = adaptive.getHistory()
        self.adaptive_history.reverse()
        self.adaptive = top_learner
        self.adaptive_settings = top_settings
        self.adaptive_acc = top_acc
        self.adaptive_setting_string  = adaptive.getSettingString(top_settings)
        if self.adaptive is not None:
            row_key = top_settings['data_type']
            self.queue.put(('statusbarset',"Training Complete, Checking Accuracy"))
            self.adaptive_acc_tuple = self._getLearnerAccuracy(self.adaptive, row_key)
            self.queue.put(('statusbarset',"Accuracy Check Complete"))
        else:
            #none of the algorithms ran, maybe timeout is to low
            self.queue.put(('statusbarset',"Adaptive failed to run. Is the timeout too low?"))
        

    def _adaptiveSetup(self):
        self._adaptiveSetupLearnerQueue()
        self.queue.put(('statusbarset',"Configuring dirac"))
        self._adaptiveSetupDirac()
        self.queue.put(('statusbarset',"Configuring tsp"))
        self._adaptiveSetupTSP()
        self.queue.put(('statusbarset',"Configuring tst"))
        self._adaptiveSetupTST()
        self.queue.put(('statusbarset',"Configuring ktsp"))
        self._adaptiveSetupKTSP()
        self.queue.put(('statusbarset',"Relational learners configured"))


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
 
       
    def clearLearningAlg(self):
        """
        Set all learning algorithms to None.
        Happens when we change something further up the dependency
        """
        self.dirac = None
        self.tsp = None
        self.tst = None
        self.ktsp = None
        self.adaptive = None
        self.tsp_acc = None
        self.ktsp_acc = None
        self.tst_acc = None
        self.dirac_acc = None
        self.adaptive_acc_tuple = None
        self.tsp_cv = None
        self.ktsp_cv = None
        self.tst_cv = None
        self.dirac_cv = None
        self.adaptive_cv = None



    def classifyDirac(self):
        dp = self.datapackage
        row_key = self.config.getSetting("dirac","Row Key(genes/probes)")[0]
        self._checkRowKey(row_key)
        self.dirac.addUnclassified(dp.getUnclassifiedDataVector(row_key ))
        self.dirac_classification = self.dirac.classify()
        return self.dirac_classification

    def classifyTSP(self):
        dp = self.datapackage
        row_key = self.config.getSetting("tsp","Row Key(genes/probes)")[0]
        self._checkRowKey(row_key)
        self.tsp.addUnclassified(dp.getUnclassifiedDataVector(row_key))
        self.tsp_classification = self.tsp.classify()
        return self.tsp_classification

    def classifyTST(self):
        dp = self.datapackage
        row_key = self.config.getSetting("tst","Row Key(genes/probes)")[0]
        self._checkRowKey(row_key)
        self.tst.addUnclassified(dp.getUnclassifiedDataVector(row_key))
        self.tst_classification = self.tst.classify()
        return self.tst_classification

    def classifykTSP(self):
        dp = self.datapackage
        row_key = self.config.getSetting("ktsp","Row Key(genes/probes)")[0]
        self._checkRowKey(row_key)
        self.ktsp.addUnclassified(dp.getUnclassifiedDataVector(row_key))
        self.ktsp_classification = self.ktsp.classify()
        return self.ktsp_classification

    def classifyAdaptive(self):
        dp = self.datapackage
        learner = self.adaptive
        settings = self.adaptive_settings
        row_key = settings['data_type']
        learner.addUnclassified(dp.getUnclassifiedDataVector(row_key))
        self.adaptive_classification = learner.classify()
        return self.adaptive_classification
 
    def crossValidateDirac(self):
        dirac = self.trainDirac(crossValidate = True)
        self.queue.put(('statusbarset',"Cross Validating"))
        self.dirac_cv = dirac.crossValidate()
        self.queue.put(('statusbarset',"Dirac had an MCC of " + str(self.dirac_cv)[:4]))

    def crossValidateTSP(self):
        tsp = self.trainTSP(crossValidate = True)
        self.queue.put(('statusbarset',"Cross Validating"))
        self.tsp_cv = tsp.crossValidate()
        self.queue.put(('statusbarset',"TSP had an MCC of " + str(self.tsp_cv)[:4]))

    def crossValidateTST(self):
        tst = self.trainTST(crossValidate = True)
        self.queue.put(('statusbarset',"Cross Validating"))
        self.tst_cv = tst.crossValidate()
        self.queue.put(('statusbarset',"TST had an MCC of " + str(self.tst_cv)[:4]))

    def crossValidateKTSP(self):
        ktsp = self.trainkTSP(crossValidate = True)
        self.queue.put(('statusbarset',"Cross Validating"))
        self.ktsp_cv = ktsp.crossValidate()
        self.queue.put(('statusbarset',"KTSP had an MCC of " + str(self.ktsp_cv)[:4]))
  
    def crossValidateAdaptive(self, target_acc, maxtime):
        self._adaptiveSetup()
        #create adaptive object
        adaptive = Adaptive(self.learnerqueue, app_status_bar = self.queue)
        self.adaptive_cv = adaptive.crossValidate(target_acc, maxtime)
        self.queue.put(('statusbarset',"Adaptive had an MCC of " + str(self.adaptive_cv)[:4]))

 
    def _checkRowKey(self, row_key, srcStr="Not Given"):
        if row_key not in ['gene', 'probe']:
            raise InputError(srcStr, "Given key " + row_key + " is invalid" )
