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

from AUREA.adaptive.LearnerQueue import LearnerQueue
import time
import os
class Adaptive:
    """
    A class to adaptively choosing a model.
    Takes a configured LearnerQueue    
    """
    def __init__(self, learnerQueue,app_status_bar = None, print_status=False):
        """
        learnerQueue is an AUREA.adaptive.LearnerQueue.LearnerQueue object
        that has had its learners defined.
        app_status_bar is an AUREA.GUI.App.StatusBar object.  If not in
            GUI then just leave it as None. 
        print_status is a boolean, if True then messages will be printed to stdout
        """
        self.lq = learnerQueue
        #app_status_bar is now thread_queue from App
        self.app_status_bar = app_status_bar
        self.print_status = print_status
        self.history = []
        self.truth_table = None

    def getLearner(self, target_acc, maxTime):
        """
        target_acc - float from (0,1] that says to stop when apparent accuracy of a model reaches that accuracy
        maxTime - maximum time in seconds to search model space
        Returns a tuple containing (achieved MCC (float), settings(dict), learner (a learner object)) the best achieved MCC for the given parameters
        """
        BAD_ACC = -.99999999

        self._progress_report("Configuring adaptive training")

        startTime = time.clock()
        self.endTime = maxTime + startTime
        self.target_accuracy = target_acc

        learners = [LearnerQueue.dirac, LearnerQueue.tsp, LearnerQueue.tst, LearnerQueue.ktsp]
        #strings for display
        viewable = ['dirac', 'tsp', 'tst', 'ktsp']        
        msg = "" #what just happened
        tl_str = "" #the best so far

        #init scores
        top_acc = BAD_ACC
        top_learner = None
        top_settings = None
    
        self._progress_report("Running Adaptive training.")
        finished = False
        str_learner = "Init:"
        for complexity, settings in self.lq:            
            est_running_time = self.lq.getEstimatedTime(settings['learner'],complexity)
            timeout = False
            est_end_time = est_running_time + time.clock()
            
            if est_end_time < self.endTime:#see if we believe we will go over
                str_learner = viewable[settings['learner']]
                self._progress_report(tl_str + msg + " Trying " + str_learner)
                
                #training
                learner = self.lq.trainLearner(settings, complexity)
                
                self._progress_report(tl_str + msg + " CrossValidating " + str_learner)
                learner.crossValidate()
                accuracy = learner.getCVAccuracy()
                mcc = learner.getCVMCC()
                
                msg = str_learner + " achieved " + str(accuracy)[:4] + "(acc) and  "
                msg += str(mcc)[:4] + "(MCC)"

                #shift accuracy to [0.0,1.0] for feedback
                #let queue know how this learner did
                self.lq.feedback(settings['learner'], (1.0+mcc)/2)
                #keep track of history for logs
                self.history.append((accuracy, settings))
            else: #our estimate says we would go over  
                timeout = True
                tl_str = str_learner + " estimated to go over time limit: "
                mcc = BAD_ACC
                learner = None
                settings = None

            #update if better
            if mcc > top_acc:
                top_acc = mcc
                top_learner = learner
                top_settings = settings
                tl_str = str_learner + " current best at " + str(top_acc)[:4] + " :"
                msg += " new top learner : "
                
            #tell why we are done
            if timeout or time.clock() > self.endTime:
                self._progress_report(tl_str + "Adaptive Finished.  Out of time.")
                finished = True
            if mcc >= self.target_accuracy:
                self._progress_report(tl_str + "Adaptive Finished.  Achieved Desired MCC.")
                finished = True

            if finished:
                break

        return (top_acc, top_settings, top_learner)

       
    def _goodEnough(self, current_accuracy):
        """
        Checks that one of the 2 conditions have been met(time or accuracy)
        True if 'good enough'
        DEPRECATED
        """
        return time.clock() > self.endTime or self.target_accuracy  <= current_accuracy

    def _progress_report(self, msg):
        """
        Takes the msg and displays it in the status bar if provided and/or prints it if print_status is True.
        """
        import time
        if self.app_status_bar is not None:
            self.app_status_bar.put( ('statusbarset', msg) )
            time.sleep(0.01)
        if self.print_status:
            print msg

    def getHistory(self):
        """
        Returns a list of tuples
        (accuracy, learner settings string)
        """
        return [(s[0], self.getSettingString(s[1])) for s in self.history]       

    def getSettingString(self, settings):
        """
        Returns a human readable version of the settings dictionary
        """
        if settings is None:
            #no algorithms ran
            return "None: Not Applicable."
        #dont want these
        ignorekeys = ['data', 'learner']
        # get a nice string with the learners name
        learnerMap = ['', '', '', '']
        learnerMap[LearnerQueue.dirac] = "DiRaC"
        learnerMap[LearnerQueue.tsp] = "TSP"
        learnerMap[LearnerQueue.tst] = "TST"
        learnerMap[LearnerQueue.ktsp] = "k-TSP"
        myStr = learnerMap[settings['learner']] + os.linesep
        
        for k, v in settings.iteritems():
            if k not in ignorekeys:
                myStr  += k + ': '
                if k == 'restrictions':
                    comma = ''
                    for r in v:
                        myStr += comma + str(r) 
                        comma = ', '
                else:
                    myStr += str(v)
                myStr += os.linesep
        return myStr

    def crossValidate(self, target_acc, maxtime, k=10):
        """
        performs kfold crossvalidation on the adaptive algorithm 
        returns the Matthews correlation coefficient
        """
        import math
        def MCC(TP,FP, TN, FN):
            den =  math.sqrt(float((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)))
            if den < .000001:
                #http://en.wikipedia.org/wiki/Matthews_correlation_coefficient
                den = 1.0
            return float(TP*TN - FP*FN)/den
        import copy
        #we swap out the base_lq, gets swapped back in at end of this meth.
        base_lq = self.lq
           
        dp = base_lq.data_package
        classifications = dp.getClassifications()
        train, test= self._partition(classifications, k)
        msg = ""
        self.truth_table = [0,0,0,0]
        for i, training_set in enumerate(train):
            T0 = 0
            F0 = 0
            T1 = 0
            F1 = 0
            #set up adaptive for this training set
            test_set = test[i]
            nLQ = self._genLearnerQueue(dp ,training_set)
            self._copyLQParams(nLQ, base_lq)
            self.lq = nLQ
            #train adaptive
            _, settings, learner = self.getLearner( float(target_acc), int(maxtime))
            msg += ": Classifying test set "+ str(i+1)
            self._progress_report("Classifying test set "+ str(i+1))
            #classify test set
            c1, c2 = test_set
            c1List = c1[1]
            c2List = c2[1]
            for table, sample in c1List:
                dp.setUnclassified(table, sample)
                lv = dp.getUnclassifiedDataVector(settings['data_type'])
                learner.addUnclassified(lv)
                pred_class = learner.classify()
                if pred_class == 0:
                    T0 += 1
                else:
                    F1 += 1
            for table, sample in c2List:
                dp.setUnclassified(table, sample)
                lv = dp.getUnclassifiedDataVector(settings['data_type'])
                learner.addUnclassified(lv)
                pred_class = learner.classify()
                if pred_class == 1:
                    T1 += 1
                else:
                    F0 += 1
            viewable = ['dirac', 'tsp', 'tst', 'ktsp']
            
            str_learner = viewable[settings['learner']]
            accuracy = float(T0+T1)/(T0+T1+F0+F1)
            mcc = MCC(T0,F0,T1,F1) 
            msg = "Adaptive(" + str_learner + ") achieved " + str(accuracy)[:4] + "(acc) and  "
            msg += str(mcc)[:4] + "(MCC)"

            self.truth_table[0] += T0
            self.truth_table[1] += T1
            self.truth_table[2] += F0
            self.truth_table[3] += F1
    
            self._progress_report(msg)
        #put things back the way they were
        self._genLearnerQueue( dp ,classifications)
        self.lq = base_lq
    
           
    def getCVAccuracy(self):
        """
        Returns the Accuracy of the last crossValidate
        """
        tpos = self.truth_table[0]
        tneg = self.truth_table[1]
        fpos = self.truth_table[2]
        fneg = self.truth_table[3] 
        return float((tpos+tneg))/(tpos+tneg+fpos+fneg)

    def getCVMCC(self):
        """
        Returns the Matthews Correlation Coefficient of the last crossValidate
        """
        import math
        tpos = self.truth_table[0]
        tneg = self.truth_table[1]
        fpos = self.truth_table[2]
        fneg = self.truth_table[3] 
        den = math.sqrt(float((tpos+fpos)*(tpos+fneg)*(tneg+fpos)*(tneg+fneg)))
        if den < .000001:#see wikipedia
            den = 1.0
        return float(tpos*tneg - fpos*fneg)/den


    def _copyLQParams(self, new_lq, base_lq):
        """
        Copies the parameters for the learners of base_lq (a Learner Queue)
        to new_lq
        """
        new_lq.genTSP(*base_lq.tsp_param)
        new_lq.genKTSP(*base_lq.ktsp_param)
        new_lq.genDirac(*base_lq.dirac_param)
        new_lq.genTST(*base_lq.tst_param)
                  


    def _partition(self,c, k):
        """
        Returns a list of (training set, test set) for the given classes
        based on k
        ts = [[(classname1, [list of (tablename, sampname) from c1]), (2 name, [list of (name, sampname) from c2])], ...]
        """
        import random
        from itertools import izip
        #initialize variables
        kfold = k
        #the ulimate returned lists
        training_list = []
        testing_list = []
        c1_size = len(c[0][1])
        c2_size = len(c[1][1])
        c1_key = c[0][0]
        c2_key = c[1][0]
        if min(c1_size, c2_size) < kfold:
            kfold = min(c1_size, c2_size)

        #first partition using indices
        c1_training_list = [[] for x in range(len(kfold))
        c1_testing_list = [[] for x in range(len(kfold))
        
        c2_training_list = [[] for x in range(len(kfold))
        c2_testing_list = [[] for x in range(len(kfold))

        #shuffle samples
        r1_list = range(c1_size)       
        r2_list = range(c2_size)
        random.shuffle(r1_list)
        random.shuffle(r2_list)
        
        #make testing lists
        for tl_pos, r1_index in enumerate(r1_list):
            list_pos = tl_pos%kfold
            c1_testing_list[list_pos].append(r1_index)

         for tl_pos, r2_index in enumerate(r2_list):
            list_pos = tl_pos%kfold
            c2_testing_list[list_pos].append(r2_index)
        #make training lists

        for training_list, testing_list in izip(c1_training_list, c1_testing_list):
            for i in r1_list:
                if i not in testing_list:
                    training_list.append(i)

 
        for training_list, testing_list in izip(c2_training_list, c2_testing_list):
            for i in r2_list:
                if i not in testing_list:
                    training_list.append(i)

        #check no bad sets
        assert(len(c1_training_list) == len(c1_testing_list))
        assert(len(c2_training_list) == len(c2_testing_list))
        def testList(tlist):
            for l in tlist:
                assert(len(l) > 0)
        testList(c1_training_list)
        testList(c1_testing_list)

        testList(c2_training_list)
        testList(c2_testing_list)

        #make actual values for return
        c1_samples = c[0][1]
        c2_samples = c[1][1]
        for i in range(kfold):
            training_ss = [(c1_key, []), (c2_key, [])]
            testing_ss = [(c1_key, []), (c2_key, [])]
            #class 1 set i
            c1_train_i = c1_training_list[i]
            for j in c1_train_i:
                training_ss[0][1].append(c1_samples[j])
            c1_test_i = c1_testing_list[i]
            for j in c1_test_i:
                testing_ss[0][1].append(c1_samples[j])
            #class 2 set i
            c2_train_i = c2_training_list[i]
            for j in c2_train_i:
                training_ss[1][1].append(c2_samples[j])
            c1_test_i = c1_testing_list[i]
            for j in c1_test_i:
                testing_ss[1][1].append(c2_samples[j])
            training_list.append(training_ss)
            testing_list.append(testing_ss)
        return (training_list, validating_list)

       
    def _genLearnerQueue(self, dataPackage, training_set):
        """
        Generates a new learnerq with the appropriate 
        data package settings from the training set
        """
        #build training package
        subset1 = training_set[0][0]
        subset2 = training_set[1][0]
        subsetSamples1 = training_set[0][1]
        subsetSamples2 = training_set[1][1]
        
        dataPackage.clearClassification()
        dataPackage.createClassification(subset1)
        dataPackage.createClassification(subset2)
        for table, sample in subsetSamples1:
            dataPackage.addToClassification( subset1, table, sample )

        for table, sample in subsetSamples2:
            dataPackage.addToClassification( subset2, table, sample )
        #build learner queue
        learner_queue = LearnerQueue(dataPackage)
        return learner_queue  



class AdaptiveTimeoutException(Exception):
    def __init__(self, msg):
        self.msg = msg
    
