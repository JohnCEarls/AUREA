from Queue import PriorityQueue
from AHREA.heuristic.ResourceEstimate import ResourceEstimate
from AHREA.learner.wilcoxon import Wilcoxon
from AHREA.learner import tsp, tst, ktsp, dirac
import time


class LearnerQueue:
    dirac = 0
    tsp = 1
    tst = 2
    ktsp = 3
    def __init__(self, data_package, wilc_data_type='probe', weight=None, scale=None, minWeight=.5 ):
        """
        This class generates a sequence of learner objects.
        Inputs:
            req:
                data_package: provide an already set up packager.DataPackage object
            optional:
                wilc_data_type: should we use probes or genes to simulate the wilcoxon process in the TSx's
                weight: A list of weights that estimated times are divided by
                scale: A list of scaling factors for the complexity estimates.
                minWeight: a weight at which to normalize the weights.
        """
        self._queue = []
        for i in range(4):#make 4 queues, 1 for each alg
            self._queue.append(PriorityQueue())
        if weight == None:
            self.weight = [1.0,1.0,1.0,1.0]
        else:
            self.weight = weight
        if scale == None:
            self.scale = [None,None,None,None]
        else:
            self.scale = scale
        self.data_package = data_package
        #estimates are based on wilc_data_type
        data, numGenes = self.data_package.getDataVector(wilc_data_type)
        _, gene_net_size = self.data_package.getGeneNetVector(0) 
        cs = self.data_package.getClassVector()
        class1size = cs[0]
        class2size = cs[1]
        self._est = ResourceEstimate( data, class1size, class2size, numGenes, gene_net_size)
        self.wilc = Wilcoxon(data, numGenes, class1size, class2size) 
        self._genQ()
        self.minWeight = minWeight 

    def __iter__(self):
        return self.next()

    def next(self):
        n = self._getNext()
        while n is not None:
            yield n
            n=self._getNext()
        raise StopIteration()

    def _genQ(self):
        for i in range(4):
            self._queue.append(PriorityQueue())

    def feedback(self, learner_id, apparent_accuracy):
        """
        Adjusts the weights of a learner.
        learner_id matching global data attribute
        apparent_accuracy - percent accuracy of learner
        """
        self._adjWeight(learner_id, apparent_accuracy)

    def genDirac(self, min_network_size, numTopNetworks, data_type='gene'):
        """
        generates the pq for dirac.
        inputs: 
            min_network_size: a tuple with (start, end, increment)
            numTopNetworks: a tuple with (start, end, increment)
        """
        self.dirac_param = (min_network_size, numTopNetworks, data_type)
        for netsize in range(*min_network_size):
            for numTop in range(*numTopNetworks):
                self._addDirac(netsize, numTop, data_type)

    def _addDirac(self, min_network_size, numTopNetworks, data_type):
        """
        Given these values, add settings and running time estimate to the
        Dirac queue.
        """
        settings = {}
        settings['learner'] = LearnerQueue.dirac
        settings['min_network_size'] = min_network_size
        settings['numTopNetworks'] = numTopNetworks
        settings['data_type'] = data_type
        data, nGenes =  self.data_package.getDataVector(data_type)
        settings['data'] = data
        settings['numGenes'] = nGenes
        self._queue[LearnerQueue.dirac].put((self._est.Diractime(min_network_size), settings))
    
    def genTSP(self, r1, r2, equijoin=False, data_type='probe'):
        """
        generates the pq for tsp.
        inputs: 
            r1 - tuple describing the range for filter 1 (from, to, increment)
            r2 - tuple describing the range for filter 2 (from, to, increment)
            equijoin - boolean, should we restrict filters to [10,10] [20,20] etc.
            
        """
        self.tsp_param = ( r1, r2, equijoin, data_type)
        _, nGenes = self.data_package.getDataVector(data_type)
    
        rest_check = {}
        for x in range(*r1):
            if x >= nGenes:
                break
            for y in range(*r2):
                if y>= nGenes:
                    break
                if not equijoin or x == y:
                    x_adj = self.wilc.filterAdjust(x)
                    y_adj = self.wilc.filterAdjust(y)
                    adj = sorted([self.wilc.filterAdjust(a) for a in [x,y]])
                    x_adj, y_adj = tuple(adj)
                    if (x_adj, y_adj) not in rest_check:
                        rest_check[(x_adj, y_adj)] = 1#keep unique after adjust
                        rVec = tsp.IntVector()
                        rVec.push_back(x_adj)
                        rVec.push_back(y_adj)
                        self._addTSP(rVec, data_type)

    def _addTSP(self, restrictions, data_type):
        """
        Given these values, add settings and running time estimate to the
        TSP queue.
        restrictions is a vector of integers that contains the filter values
        data_type is probe/gene
        """
        settings = {}
        settings['learner'] = LearnerQueue.tsp
        settings['restrictions'] = restrictions
        settings['data_type'] = data_type
        data, nGenes = self.data_package.getDataVector(data_type)
        settings['data'] = data
        settings['numGenes'] = nGenes
        self._queue[LearnerQueue.tsp].put((self._est.TSPtime(restrictions), settings))

    def genTST(self, r1, r2, r3, equijoin=False, data_type='probe'):
        """
        generates the pq for tst
        inputs: 
            r1 - tuple describing the range for filter 1 (from, to, increment)
            r2 - tuple describing the range for filter 2 (from, to, increment)
            r3 - tuple describing the range for filter 3 (from, to, increment)
            equijoin - boolean, should we restrict filters to [10,10] [20,20] etc.
            
        """
        self.tst_param = ( r1, r2, r3, equijoin, data_type)
        _, nGenes = self.data_package.getDataVector(data_type)
        rest_check = {}
        for x in range(*r1):
            if x >= nGenes:
                break #GIGO - bad range
            for y in range(*r2):
                if y >= nGenes:
                    break
                for z in range(*r3):
                    if z >= nGenes: 
                        break
                    if not equijoin or x == y == z:
                        adj = sorted([self.wilc.filterAdjust(a) for a in [x,y,z]])
                        x_adj, y_adj, z_adj = tuple(adj)
                        if (x_adj, y_adj, z_adj) not in rest_check:
                            #rest_check (don't want duplicates)
                            rest_check[(x_adj, y_adj, z_adj)] = 1
                            rVec = tsp.IntVector()
                            rVec.push_back(x_adj)
                            rVec.push_back(y_adj)
                            rVec.push_back(z_adj)
                            self._addTST(rVec, data_type)


    def _addTST(self, restrictions, data_type):
        """
        Given these values, add settings and running time estimate to the
        TSP queue.
        restrictions is a vector of integers that contains the filter values
        data_type is probe/gene
        """
        settings = {}
        settings['learner'] = LearnerQueue.tst
        settings['restrictions'] = restrictions
        settings['data_type'] = data_type
        data, nGenes = self.data_package.getDataVector(data_type)
        settings['data'] = data
        settings['numGenes'] = nGenes
        self._queue[LearnerQueue.tst].put((self._est.TSTtime(restrictions), settings))

    def genKTSP(self, maxK, ncv, nlo, r1, r2, equijoin=False, data_type='probe'):
        """
        generates the pq for tst
        inputs:
            maxK - tuple describing the range for the maximum k value
            ncv - tuple describing the range for number of cross validations
            nlo - tuple describing the range for number of elements to leave out of internal crossvalidation 
            r1 - tuple describing the range for filter 1 (from, to, increment)
            r2 - tuple describing the range for filter 2 (from, to, increment)
            equijoin - boolean, should we restrict filters to [10,10] [20,20] etc.
            
        """
        self.ktsp_param =  (r1, r2, equijoin, data_type)
        _, nGenes = self.data_package.getDataVector(data_type)
        rest_check = {}
        for x in range(*r1):
            if x >= nGenes:
                break
            for y in range(*r2):
                if y>= nGenes:
                    break
                if not equijoin or x == y:
                    x_adj = self.wilc.filterAdjust(x)
                    y_adj = self.wilc.filterAdjust(y)
                    if (x_adj, y_adj) not in rest_check:
                        rest_check[(x_adj, y_adj)] = 1#keep unique
                        rVec = tsp.IntVector()
                        rVec.push_back(x_adj)
                        rVec.push_back(y_adj)
                        for k in range(*maxK):
                            for cv in range(*ncv):
                                for n in range(*nlo):
                                    self._addKTSP(k, cv, n, rVec, data_type)


    def _addKTSP(self, maxk, num_cross_validate, num_leave_out, restrictions, data_type='probe'):
        """
        Given these values, add settings and running time estimate to the
        TSP queue.
        restrictions is a vector of integers that contains the filter values
        data_type is probe/gene
        
        """
        settings = {}
        settings['learner'] = LearnerQueue.ktsp
        settings['restrictions'] = restrictions
        settings['maxk'] = maxk
        settings['num_leave_out'] = num_leave_out
        settings['num_cross_validate'] = num_cross_validate
        settings['data_type'] = data_type
        data, nGenes = self.data_package.getDataVector(data_type)
        settings['data'] = data
        settings['numGenes'] = nGenes
        self._queue[LearnerQueue.ktsp].put((self._est.kTSPtime(maxk, num_cross_validate, restrictions), settings))


    def _calcScale(self, real_time, estimated_time):
        #print "real time: ",
        #print real_time
        return estimated_time/real_time

    def _adjWeight(self, learner, score):
        """
        Adjusts the given learners weight by the product of the given score
        """
        self.weight[learner] = score*self.weight[learner]
        if self.weight[learner] < self.minWeight:
            self._normalizeWeight()

    def _adjScale(self, learner, scale):
        self.scale[learner] = scale

    def _normalizeWeight(self):
        """
        Divide all weights by the max weight to rescale the weights.
        """
        wMax = max(self.weight)
        self.weight = [x/wMax for x in self.weight]
        wMin = min(self.weight)
        self.minWeight = wMin/2.0

    def _getNext(self):
        poss = []
        min = float('inf')
        curr = None
        for x in range(4):
            #cycle through the queues looking for the best score
            if not self._queue[x].empty():
                next = self._queue[x].get()
                #scale time to last observed
                if self.scale[x] is None:
                    #initially scale all to .01 sec
                    self.scale[x] = 100*float(next[0])
                adj_next = next[0]/(self.weight[x]*self.scale[x])
                if adj_next < min:
                    min = adj_next
                    if curr is not None:#put previous best back
                        self._queue[curr[1]['learner']].put(curr)
                    curr = next 
                else:
                    self._queue[x].put(next)
        return curr 

    def trainLearner(self, settings, est_time):
        """
        Returns a learner that has been trained according to the settings given.
        """
        start = time.clock()
        l =  self.getLearner(settings)
        l.train()
        real_time = time.clock() - start
        newScale = 1.0
        if real_time > 0.0:#should not happen, but windows may be silly
            newScale = self._calcScale(real_time, est_time)
        self._adjScale(settings['learner'], newScale)       
        return l

 
    def getLearner(self, settings):
        """
        Returns a learner object corresponding to the provided settings dict.
        """
        if settings['learner'] == LearnerQueue.tsp:
            data = settings['data']
            numGenes = settings['numGenes']
            classSizes = self.data_package.getClassVector()
            filter = settings['restrictions']
            return tsp.TSP(data, numGenes, classSizes, filter)

        if settings['learner'] == LearnerQueue.tst:
            data = settings['data']
            numGenes = settings['numGenes']
            classSizes = self.data_package.getClassVector()
            filter = settings['restrictions']
            return tst.TST(data, numGenes, classSizes, filter)
  
        if settings['learner'] == LearnerQueue.ktsp:
            data = settings['data']
            numGenes = settings['numGenes']
            classSizes = self.data_package.getClassVector()
            filter = settings['restrictions']
            maximumK = settings['maxk']
            nleaveout = settings['num_leave_out']
            nValidationRuns = settings['num_cross_validate'] 
            return ktsp.KTSP(data, numGenes, classSizes, filter, maximumK, nleaveout, nValidationRuns) 
 
        if settings['learner'] == LearnerQueue.dirac:
            data = settings['data']
            numGenes = settings['numGenes']
            classSizes = self.data_package.getClassVector()
            #clear out old gene net and create new one
            self.data_package.createGeneNetVector(settings['min_network_size'])
            geneNet, geneNetSize = self.data_package.getGeneNetVector(settings['min_network_size'])
            numnet = settings['numTopNetworks']
            geneNetMap = self.data_package.gene_net_map
            return dirac.Dirac(data, numGenes, classSizes, geneNet, geneNetSize,numnet, geneNetMap )    

        raise Exception("Unrecognized learner")
