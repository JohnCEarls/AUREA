from AHREA.heuristic.LearnerQueue import LearnerQueue
import time
import os
class Adaptive:
    """
    A class to adaptively choosing a model.
    Takes a configured LearnerQueue    
    """
    def __init__(self, learnerQueue):
        self.lq = learnerQueue       

    def getLearner(self, target_acc, maxTime):
        """
        target_acc - float from (0,1] that says to stop when apparent accuracy of a model reaches that accuracy
        maxTime - maximum time in seconds to search model space
        Returns a tuple containing (achieved accuracy (float), settings(dict), learner (a learner object)) the best achieved accuracy for the given parameters
        """
        startTime = time.time()
        self.endTime = maxTime + startTime
        self.target_accuracy = target_acc
        learners = [LearnerQueue.dirac, LearnerQueue.tsp, LearnerQueue.tst, LearnerQueue.ktsp]
        top_acc = .000001
        top_learner = None
        top_settings = None
        for est_running_time, settings in self.lq:
            #train
            learner = self.learnerqueue.trainLearner(settings, est_running_time)
            #cross validation
            if settings['learner'] != LearnerQueue.dirac:
                accuracy = learner.crossValidate()
            else:
                accuracy = learner.crossValidate(numTopNetworks=settings['numTopNetworks'])
            #update if better
            if accuracy > top_acc:
                top_acc = accuracy
                top_learner = learner
                top_settings = settings
            #let queue know how this learner did
            self.learnerqueue.feedback(settings['learner'], accuracy)
            if self._goodEnough(accuracy):
                break
        if top_learner == None:
            raise Exception("No Learner found, this should not happen")
        return (top_acc, top_settings, top_learner)

       
    def _goodEnough(self, current_accuracy):
        return time.time() > self.endTime or self.target_accuracy  <= current_accuracy

        
       
