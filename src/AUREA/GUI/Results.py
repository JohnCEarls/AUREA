"""
Copyright (C) 2011  N.D. Price Lab

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from Tkinter import *
import tkFileDialog
import os
from AUREA.adaptive.LearnerQueue import LearnerQueue
from itertools import izip_longest
class Results(Toplevel):
    """
    Base class for the results popups
    """
    def __init__(self,root):
        Toplevel.__init__(self)
        self.root = root
        self.position()

    def position(self):
        self.transient(self.root)
        self.geometry("+%d+%d" % (self.root.winfo_rootx()+50,
        self.root.winfo_rooty()+50))

    def getDataInfoString(self):
        """
        Generating some more text information for the saved output
        This is general stuff, sample names, classes

        returns formatted string 
        """
        cont = self.root.root.controller
        dp = cont.datapackage
        #describe input data
        classifications = dp.getClassifications()
        retStr = '\nTraining Samples\n'
        if len(classifications) > 0:
            c1, c2 = classifications
            retStr += c1[0] + '\t' + c2[0] + '\n'#class names
            retStr += '='*10 + '\t' + '='*10 + '\n'
            for c1_samp, c2_samp in izip_longest(c1[1], c2[1], fillvalue=('-','-')):
                retStr += c1_samp[0] + '.'+ c1_samp[1] + '\t'
                retStr += c2_samp[0] + '.'+ c2_samp[1] + '\n'
            retStr += '\n' 

        return retStr

    def getSettingsInfoString(self, learner=None):
        """
        This returns the settings information for the data and a learner
        
        """
        retStr = ''
        retStr += '\n\nSettings\n'
        retStr += '='*20 + '\n'
        retStr += 'Data Settings' + '\n'
        
        cont = self.root.root.controller
        for name, values in cont.config.getSettings('datatable'):
            v = ','.join(map(str,values))
            retStr += name + ':' + v + '\n'
        if learner is not None:
            retStr += '\n' + learner.upper() + ' Settings\n'
            retStr += '='*20 + '\n'
            for name, values in cont.config.getSettings(learner):
                v = ','.join(map(str,values))
                retStr += name + ':' + v + '\n'
        return retStr 

        


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
            o.write(resultString + '\n' + self.getDataInfoString())
            o.close()

class DiracResults(Results):
    def __init__( self, root ):
        Results.__init__(self, root)
        self.title("AUREA: Dirac results")
        self.getData()
        self.displayTopNetworks()


    def getData(self):
        c = self.root.root.controller
        self.dirac = c.dirac
        self.accuracy = c._acc(c.dirac_acc)
        self.datapackage = c.datapackage
        self.config = c.config
        
        
    def displayTopNetworks(self):
        tn = self.dirac.getTopNetworks()
        rc = self.dirac.getRankConservation()
        rc_dict = {}
        for i, rcs in enumerate(rc):
            rc_dict[self.dirac.netMap[i]] = map(str,rcs)
        #print rc
        resultString = ""
        resultString += "@acc: " + str(self.accuracy) + os.linesep
        num_net = self.config.getSetting("dirac","Number of Top Networks")[0]
        
        tn = tn[0:num_net]
        network_listbox = Listbox(self)
        for net in tn:
            network_listbox.insert(END, net)
            resultString += "*"*20 + os.linesep
            resultString += net + os.linesep
            resultString += "Rank Conservation Scores: " + ','.join(map(str,rc_dict[net])) + os.linesep
            resultString += "Genes used: " + ','.join(self.datapackage.getGeneNamesFromNetwork(net))+os.linesep
            
        network_listbox.pack()
        resultString += self.getSettingsInfoString('dirac')
        save_button = Button(self, text="Save...", command=lambda:self.saveResults(resultString))
        save_button.pack()

     
class TSPResults(Results):
    def __init__(self, root ):
        Results.__init__(self, root)
        self.root = root
        self.getData()
        self.displayData()
    
    def getData(self):
        c = self.root.root.controller
        self.tsp = c.tsp
        self.accuracy = c._acc(c.tsp_acc)
        self.datapackage = c.datapackage
        self.config = c.config
        
    def displayData(self):
        ms = self.tsp.getMaxScores()
        row = 1
        row_key = self.config.getSetting("tsp","Row Key(genes/probes)")[0]
        resultString = "" 
        resultString += "@acc: " + str(self.accuracy) + os.linesep
        resultString += "Note: Assigns to class 1 if gene1 is more expressed than gene2" + os.linesep
        
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
        Label(self, text="Note: Assigns to class 1 if gene1 is more expressed than gene2").grid(row=row, column=0, columnspan=2)
        row += 1
        resultString += self.getSettingsInfoString('tsp')
        save_button = Button(self, text="Save...", command=lambda:self.saveResults(resultString))
 
        save_button.grid(row=row, column=1, sticky=E)

 
class TSTResults(Results):
    def __init__(self, root):
        Results.__init__(self, root)
        self.getData()
        self.displayData()

    def getData(self):
        c = self.root.root.controller
        self.tst = c.tst
        self.accuracy = c._acc(c.tst_acc)
        self.datapackage = c.datapackage
        self.config = c.config
 
    def getPtableString(self):
        ptable = self.tst.ptable
        ptStr = 'order\tP(order|class1)\tP(order|class2) ' + os.linesep
        ord = ['g1<g2<g3', 'g1<g3<g2', 'g2<g1<g3', 'g2<g3<g1', 'g3<g1<g2', 'g3<g2<g1']
        for t, triplet in enumerate(ptable):
            ptStr += "Triplet " + str(t+1) + os.linesep
            c1 = triplet[0]
            c2 = triplet[1]
            for i in range(6):
                ptStr += ord[i]
                ptStr += '\t'
                ptStr += str(c1[i])
                ptStr += '\t'
                ptStr += str(c2[i])
                ptStr += os.linesep
        return ptStr

    def displayData(self):
        ms = self.tst.getMaxScores()
        row = 1
        row_key = self.config.getSetting("tst","Row Key(genes/probes)")[0]
        resultString = "" 
        resultString += "@acc: " + str(self.accuracy) + os.linesep
        for genes in ms:
            column = 0
            tab = ''
            for i,gene in enumerate(genes):
                gene_name = self.datapackage.getGeneName(gene, row_key)
                resultString += tab + 'g'+str(i+1)+'=' + gene_name
                Label(self,text=gene_name).grid(row=row, column=column, padx=10 )
                tab = '\t'
                column += 1
            resultString += os.linesep
            row += 1
        resultString += self.getPtableString()
        Label(self, text="Note: Save and view created file to see the probability tables used for classification.").grid(row=row, column=0, columnspan=3)
        row += 1
        resultString += self.getSettingsInfoString('tst')
        save_button = Button(self, text="Save...", command=lambda:self.saveResults(resultString))
        save_button.grid(row=row, column=2, sticky=E)

 

class KTSPResults(Results):
    def __init__(self, root):
        Results.__init__(self, root)
        self.root = root
        self.getData()
        self.displayData()
    def getData(self):
        c = self.root.root.controller
        self.ktsp = c.ktsp
        self.accuracy = c._acc(c.ktsp_acc)
        self.datapackage = c.datapackage
        self.config = c.config
 
    def displayData(self):
        topk = self.ktsp.getMaxScores()
        row = 1
        row_key = self.config.getSetting("ktsp","Row Key(genes/probes)")[0]
        resultString = "" 
        resultString += "Note: Assigns to class 1 if gene1 is more expressed than gene2"
        resultString += "@acc: " + str(self.accuracy) + os.linesep
        for genes in topk:
            column = 0
            tab = ''
            genes = (genes[0], genes[1])
            for gene in genes:
                gene_name = self.datapackage.getGeneName(gene, row_key)
                resultString += tab + gene_name
                Label(self,text=gene_name).grid(row=row, column=column, padx=10 )
                tab = '\t'
                column += 1
            resultString += os.linesep
            row += 1
        Label(self, text="Note: Assigns to class 1 if gene1 is more expressed than gene2").grid(row=row, column=0, columnspan=2)
        row += 1
        resultString += self.getSettingsInfoString('ktsp')
        save_button = Button(self, text="Save...", command=lambda:self.saveResults(resultString))
        save_button.grid(row=row, column=1, sticky=E)

class AdaptiveResults(Results):
    def __init__(self,root):
        Results.__init__(self, root)
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
        t1, t2, f1,f2 = c.adaptive_acc
        strAcc = str(float(t1+t2)/(t1+t2+f1+f2))
        resultStr = "Top Learner : " + learnerMap[winner] + "@acc: " +strAcc + os.linesep
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
            resultStr += "*"*30 + os.linesep
            resultStr += "@accuracy:"+str(acc) + os.linesep
            resultStr += txt
        
        resultStr += self.getSettingsInfoString('adaptive')
             
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


class ClassificationResults(Results):
    def __init__(self, root):
        Results.__init__(self, root)

    def getStats(self, res):
        import math
        def MCC(TP,FP, TN, FN):
            den = math.sqrt(float((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)))
            if den < .000001:
                #http://en.wikipedia.org/wiki/Matthews_correlation_coefficient
                den = 1.0
            return float(TP*TN - FP*FN)/den
        T0 = 0
        F0 = 0
        T1 = 0
        F1 = 0
        for pred, act, table, sample in res:
            if pred == 0:
                if act == 0:
                    T0 += 1
                else:
                    F0 += 1
            else:
                if act == 1:
                    T1 += 1
                else:
                    F1 += 1
        mcc = MCC(T0,F0,T1,F1)
        return  (T0, F0, T1, F1, mcc)

    def getStatsString(self, res):
        T0, F0, T1, F1, mcc = self.getStats(res)
        sString = os.linesep*2
        sString += "Accuracy" + os.linesep
        sString += "="*(len(sString) -1)
        sString += os.linesep
        sString += "True class 1: " + str(T0) + os.linesep
        sString += "False class 1: " + str(F0) + os.linesep
        sString += "True class 2: " + str(T1) + os.linesep
        sString += "False class 2: " + str(F1) + os.linesep
        sString += "Matthew's Correlation: " + str(mcc)[:5] + os.linesep
        sString += "Accuracy: " + str(float(T0+T1)/(T0+T1+F0+F1))[:5] + os.linesep
        return sString
    
    def getOutputString(self, res):
        outStr = self.getClassifierString()
        outStr += self.getResultsString(res)
        return outStr


    def getResultsString(self, res):
        c1_name =self.root.root.controller.class1name
        c2_name = self.root.root.controller.class2name
        rStr = self.getStatsString(res)
        rStr += os.linesep*2
        rStr += "table\tsample\tActual\tClassification\tCorrect" + os.linesep
        for pred, act, table, sample in res:
            if pred == 0:
                predstr = c1_name
            else:
                predstr = c2_name
            if act == 0:
                actstr = c1_name
            else:
                actstr = c2_name
            
            rStr += table + '\t'
            rStr += sample + '\t'
            rStr += actstr + '\t'
            rStr += predstr + '\t'
            rStr += '+' if pred == act else '-'
            rStr += os.linesep
        return rStr
            
class DiracClassificationResults(ClassificationResults):
    def __init__(self, root):
        ClassificationResults.__init__(self, root)
        self.getData()
        self.buildDisplay()

    def getData(self):
        self.dirac = self.root.root.controller.dirac
        self.dirac_results = self.root.root.controller.dirac_classified_results
        self.datapackage = self.root.root.controller.datapackage

    def buildDisplay(self):
        c1_name =self.root.root.controller.class1name
        c2_name = self.root.root.controller.class2name
        Label(self, text="Dirac Classification Results").grid(row=0, column =0, sticky=W)
        T0, F0, T1, F1, mcc = self.getStats(self.dirac_results)
        statString = ["True " + c1_name + ": " + str(T0), "False " + c1_name  + ": " + str(F0), "True " + c2_name  + ": " + str(T1),"False " + c2_name  + ": " + str(F1), "MCC: " + str(mcc)[:5]]
        for i,ss in enumerate(statString):
            Label(self, text=ss).grid( row=i+1, column=0, sticky=W)
        
        Label(self, text="For Complete Results, Save and view textfile").grid(row=6, column=0, sticky=W)
        ostring = self.getOutputString(self.dirac_results)
        Button(self, text="Save", command=lambda:self.saveResults(ostring)).grid(row=7,column=0, sticky=E)

    def getClassifierString(self):
        resultStr = "Dirac Classification Results" + os.linesep
        resultStr += "="*(len(resultStr) - 1)
        resultStr += os.linesep
        resultStr += "Using the following networks for classification:"
        resultStr += os.linesep
        tn = self.dirac.getTopNetworks()
        for net in tn:
            resultStr += net + os.linesep
        return resultStr          
 
 
class TSPClassificationResults(ClassificationResults):
    def __init__(self, root):
        ClassificationResults.__init__(self, root)
        self.getData()
        self.buildDisplay()

    def getData(self):
        self.tsp = self.root.root.controller.tsp
        self.tsp_results = self.root.root.controller.tsp_classified_results
        self.datapackage = self.root.root.controller.datapackage
        self.config = self.root.root.controller.config

    def buildDisplay(self):
        c1_name =self.root.root.controller.class1name
        c2_name = self.root.root.controller.class2name
        Label(self, text="TSP Classification Results").grid(row=0, column =0, sticky=W)
        T0, F0, T1, F1, mcc = self.getStats(self.tsp_results)
        statString = ["True " + c1_name + ": " + str(T0), "False " + c1_name  + ": " + str(F0), "True " + c2_name  + ": " + str(T1),"False " + c2_name  + ": " + str(F1), "MCC: " + str(mcc)[:5]]
        for i,ss in enumerate(statString):
            Label(self, text=ss).grid( row=i+1, column=0, sticky=W)
        
        Label(self, text="For Complete Results, Save and view textfile").grid(row=6, column=0, sticky=W)
        ostring = self.getOutputString(self.tsp_results)
        Button(self, text="Save", command=lambda:self.saveResults(ostring)).grid(row=7,column=0, sticky=E)


        save_button = Button(self, command=lambda:self.saveResults(ostring))

    def getClassifierString(self):
        resultStr = "TSP Classification Results" + os.linesep
        resultStr += "="*(len(resultStr) - 1)
        resultStr += os.linesep
        resultStr += "Using the following genes for classification:"
        resultStr += os.linesep
        resultStr += "Note: Assigns to class 1 if gene1 is more expressed than gene2" + os.linesep
        row_key = self.config.getSetting("tsp","Row Key(genes/probes)")[0]
        ms = self.tsp.getMaxScores()
        for genes in ms:
            column = 0
            tab = ''
            for gene in genes:
                gene_name = self.datapackage.getGeneName(gene, row_key)
                resultStr += tab + gene_name
                tab = '\t'
                column += 1
            resultStr += os.linesep
        resultStr += os.linesep 
        return resultStr          
 
class KTSPClassificationResults(ClassificationResults):
    def __init__(self, root):
        ClassificationResults.__init__(self, root)
        self.getData()
        self.buildDisplay()

    def getData(self):
        self.ktsp = self.root.root.controller.ktsp
        self.ktsp_results = self.root.root.controller.ktsp_classified_results
        self.datapackage = self.root.root.controller.datapackage
        self.config = self.root.root.controller.config

    def buildDisplay(self):
        c1_name =self.root.root.controller.class1name
        c2_name = self.root.root.controller.class2name
        Label(self, text="KTSP Classification Results").grid(row=0, column =0, sticky=W)
        T0, F0, T1, F1, mcc = self.getStats(self.ktsp_results)
        statString = ["True " + c1_name + ": " + str(T0), "False " + c1_name  + ": " + str(F0), "True " + c2_name  + ": " + str(T1),"False " + c2_name  + ": " + str(F1), "MCC: " + str(mcc)[:5]]
        for i,ss in enumerate(statString):
            Label(self, text=ss).grid( row=i+1, column=0, sticky=W)
        
        Label(self, text="For Complete Results, Save and view textfile").grid(row=6, column=0, sticky=W)
        ostring = self.getOutputString(self.ktsp_results)
        Button(self, text="Save", command=lambda:self.saveResults(ostring)).grid(row=7,column=0, sticky=E)


        save_button = Button(self, command=lambda:self.saveResults(ostring))

    def getClassifierString(self):
        resultStr = "TSP Classification Results" + os.linesep
        resultStr += "="*(len(resultStr) - 1)
        resultStr += os.linesep
        resultStr += "Using the following genes for classification:"
        resultStr += os.linesep
        resultStr += "Note: Assigns to class 1 if gene1 is more expressed than gene2" + os.linesep
        row_key = self.config.getSetting("ktsp","Row Key(genes/probes)")[0]
        ms = self.ktsp.getMaxScores()
        for genes in ms:
            column = 0
            tab = ''
            for gene in genes:
                gene_name = self.datapackage.getGeneName(gene, row_key)
                resultStr+= tab + gene_name
                tab = '\t'
                column += 1
            resultStr+= os.linesep
        resultStr+= os.linesep 
        return resultStr          
  
 
class TSTClassificationResults(ClassificationResults):
    def __init__(self, root):
        ClassificationResults.__init__(self, root)
        self.getData()
        self.buildDisplay()

    def getData(self):
        self.tst = self.root.root.controller.tst
        self.tst_results = self.root.root.controller.tst_classified_results
        self.datapackage = self.root.root.controller.datapackage
        self.config = self.root.root.controller.config

    def buildDisplay(self):
        c1_name =self.root.root.controller.class1name
        c2_name = self.root.root.controller.class2name
        Label(self, text="TST Classification Results").grid(row=0, column =0, sticky=W)
        T0, F0, T1, F1, mcc = self.getStats(self.tst_results)
        statString = ["True " + c1_name + ": " + str(T0), "False " + c1_name  + ": " + str(F0), "True " + c2_name  + ": " + str(T1),"False " + c2_name  + ": " + str(F1), "MCC: " + str(mcc)[:5]]
        for i,ss in enumerate(statString):
            Label(self, text=ss).grid( row=i+1, column=0, sticky=W)
        
        Label(self, text="For Complete Results, Save and view textfile").grid(row=6, column=0, sticky=W)
        ostring = self.getOutputString(self.tst_results)
        Button(self, text="Save", command=lambda:self.saveResults(ostring)).grid(row=7,column=0, sticky=E)


        save_button = Button(self, command=lambda:self.saveResults(ostring))

    def getClassifierString(self):
        resultStr = "TSP Classification Results" + os.linesep
        resultStr += "="*(len(resultStr) - 1)
        resultStr += os.linesep
        resultStr += "Using the following genes for classification:"
        resultStr += os.linesep
        resultStr += "Note: Assigns to class 1 if gene1 is more expressed than gene2" + os.linesep
        row_key = self.config.getSetting("tst","Row Key(genes/probes)")[0]
        ms = self.tst.getMaxScores()
        for genes in ms:
            column = 0
            tab = ''
            for gene in genes:
                gene_name = self.datapackage.getGeneName(gene, row_key)
                resultStr+= tab + gene_name
                tab = '\t'
                column += 1
            resultStr+= os.linesep
        resultStr += os.linesep 
        return resultStr          
 

 
class AdaptiveClassificationResults(ClassificationResults):
    def __init__(self, root):
        ClassificationResults.__init__(self, root)
        self.getData()
        self.buildDisplay()

    def getData(self):
        self.adaptive = self.root.root.controller.adaptive
        self.adaptive_results = self.root.root.controller.adaptive_classified_results
        self.datapackage = self.root.root.controller.datapackage
        self.config = self.root.root.controller.config

    def buildDisplay(self):
        c1_name =self.root.root.controller.class1name
        c2_name = self.root.root.controller.class2name
        Label(self, text="Adaptive Classification Results").grid(row=0, column =0, sticky=W)
        T0, F0, T1, F1, mcc = self.getStats(self.adaptive_results)
        statString = ["True " + c1_name + ": " + str(T0), "False " + c1_name  + ": " + str(F0), "True " + c2_name  + ": " + str(T1),"False " + c2_name  + ": " + str(F1), "MCC: " + str(mcc)[:5]]
        for i,ss in enumerate(statString):
            Label(self, text=ss).grid( row=i+1, column=0, sticky=W)
        
        Label(self, text="For Complete Results, Save and view textfile").grid(row=6, column=0, sticky=W)
        ostring = self.getOutputString(self.adaptive_results)
        Button(self, text="Save", command=lambda:self.saveResults(ostring)).grid(row=7,column=0, sticky=E)


        save_button = Button(self, command=lambda:self.saveResults(ostring))

    def getClassifierString(self):
        #in order to get the classifier string we need to know what sort of 
        #learning alg we are working with
        learnerMap = ['', '', '', '']
        learnerMap[LearnerQueue.dirac] = "DiRaC"
        learnerMap[LearnerQueue.tsp] = "TSP"
        learnerMap[LearnerQueue.tst] = "TST"
        learnerMap[LearnerQueue.ktsp] = "k-TSP"
        self.datapackage = self.root.root.controller.datapackage
        c = self.root.root.controller
        winner = c.adaptive_settings['learner']
        
        resultStr = "Adaptive Classification Results" + os.linesep
        resultStr += "="*(len(resultStr) - 1)
        resultStr += os.linesep
        resultStr = "Using Learner : " + learnerMap[winner] +  os.linesep
        resultStr = "See Adaptive more info  on homepage for more information"
        resultStr += os.linesep
        if winner == LearnerQueue.dirac:
            tn = c.adaptive.getTopNetworks()
            
            for net in tn:                
                resultStr += net + os.linesep
        else:
            l = c.adaptive.getMaxScores()
            row_key = c.adaptive_settings['data_type'] 
            for genes in l:
                tab = ''
                for gene in genes:
                    gene_name = self.datapackage.getGeneName(gene, row_key)
                    resultStr += tab + gene_name
                    tab = '\t'
                resultStr += os.linesep
        resultStr += c.adaptive_setting_string 

        return resultStr

