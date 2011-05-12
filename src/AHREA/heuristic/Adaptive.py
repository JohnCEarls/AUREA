from AHREA.heuristic.LearnerQueue import LearnerQueue
import time
import os
class Adaptive:
    """
    A class to adaptively choosing a model.
    Takes a configured LearnerQueue    
    """
    def __init__(self, learnerQueue,app_status_bar = None, print_status=False):
        """
        learnerQueue is an AHREA.heuristic.LearnerQueue.LearnerQueue object
        that has had its learners defined.
        app_status_bar is an AHREA.GUI.AHREAApp.StatusBar object.  If not in
            GUI then just leave it as None. 
        print_status is a boolean, if True then messages will be printed to stdout
        """
        self.lq = learnerQueue
        self.app_status_bar = app_status_bar
        self.print_status = print_status
        self.history = []

    def getLearner(self, target_acc, maxTime):
        """
        target_acc - float from (0,1] that says to stop when apparent accuracy of a model reaches that accuracy
        maxTime - maximum time in seconds to search model space
        Returns a tuple containing (achieved accuracy (float), settings(dict), learner (a learner object)) the best achieved accuracy for the given parameters
        """
        #signal to catch timeouts
        import signal
        from AHREA.heuristic.Adaptive import AdaptiveTimeoutException
        def signal_handler(signum, frame):
            """
            TYVM
            http://stackoverflow.com/questions/366682/how-to-limit-execution-time-of-a-function-call-in-python
            """
            raise AdaptiveTimeoutException("Timed out")
        signal.signal(signal.SIGALRM, signal_handler)
        self._progress_report("Configuring adaptive training")
        #check settings, if bad use defaults
        try:
            acc = float(target_acc)
        except Exception:
            acc = .9
        if acc > 1.0 or acc <= .0:
            acc = .9
        try:
            mtime = int(maxTime)
        except:
            mtime = 2**20
        startTime = time.clock()
        self.endTime = maxTime + startTime
        self.target_accuracy = acc

        learners = [LearnerQueue.dirac, LearnerQueue.tsp, LearnerQueue.tst, LearnerQueue.ktsp]
        #strings for display
        viewable = ['dirac', 'tsp', 'tst', 'ktsp']        
        msg = "" #what just happened
        tl_str = "" #the best so far

        #init scores
        top_acc = .000001
        top_learner = None
        top_settings = None
    
        self._progress_report("Running Adaptive training.")
        for est_running_time, settings in self.lq:
            timeout = False
            str_learner = viewable[settings['learner']]
            #training
            self._progress_report(tl_str + msg + " Trying " + str_learner)
            
            #set up alarm in case training learner goes over time
            signal.alarm( int( self.endTime - time.clock() ) + 1)
            try:            
                learner = self.lq.trainLearner(settings, est_running_time)
                signal.alarm(0)#made it
            except AdaptiveTimeoutException: 
                timeout = True
                signal.alarm(0)

            #cross validation
            if timeout:
                msg = str_learner + " timed out. :"
                accuracy = .001
                learner = None
                settings = None
            else:
                accuracy = learner.crossValidate()
                msg = str_learner + " achieved " + str(accuracy)[:4]
            #update if better
            if accuracy > top_acc:
                top_acc = accuracy
                top_learner = learner
                top_settings = settings
                tl_str = str_learner + " current best at " + str(top_acc)[:4] + " :"
                msg += " new top learner : "
            #let queue know how this learner did
            if settings is not None:
                #shift accuracy to [0.0,1.0]
                self.lq.feedback(settings['learner'], (1.0+accuracy)/2)
                #keep track of history
                self.history.append((accuracy, settings))
                
            if self._goodEnough(accuracy):
                #tell why we are done
                if time.clock() > self.endTime:
                    self._progress_report(tl_str + "Adaptive Finished.  Out of time.")
                if accuracy >= self.target_accuracy:
                    self._progress_report(tl_str + "Adaptive Finished.  Achieved Desired MCC.")
                break
        return (top_acc, top_settings, top_learner)

       
    def _goodEnough(self, current_accuracy):
        return time.clock() > self.endTime or self.target_accuracy  <= current_accuracy

    def _progress_report(self, msg):
        """
        Takes the msg and displays it in the status bar if provided and/or prints it if print_status is True.
        """
        if self.app_status_bar is not None:
            self.app_status_bar.set( msg )
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

class AdaptiveTimeoutException(Exception):
    def __init__(self, msg):
        self.msg = msg
    
