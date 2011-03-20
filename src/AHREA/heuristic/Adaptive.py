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
        startTime = time.time()
        sekf.endTime = maxTime + startTime
        self.target_accuracy = target_acc
        learners = [LearnerQueue.dirac, LearnerQueue.tsp, LearnerQueue.tst, LearnerQueue.ktsp]
        top_acc = .000001
        top_learner = None
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
            #let queue know how this learner did
            self.learnerqueue.feedback(settings['learner'], accuracy)
            if self._goodEnough(accuracy):
                break
        return (top_acc, top_learner)

       
    def _goodEnough(self, current_accuracy):
        return time.time() > self.endTime or self.target_accuracy  <= current_accuracy

        
       
