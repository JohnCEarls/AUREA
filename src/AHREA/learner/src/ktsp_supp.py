%pythoncode{
class KTSP:
    def __init__(self, data, numGenes, classSizes, filters, maximumK, nleaveout, nValidationRuns):
        self.data = data
        self.numGenes = numGenes
        self.classSizes = classSizes
         
        self.filters = filters
        self.maximumK = maximumK
        self.nleaveout = nleaveout
        self.nValidationRuns = nValidationRuns
        self.topKPairs = []
        self._checkFilters()

    def _checkFilters(self):
        """
        Checks that the filters are not set so low that there
        are not enough disjoint pairs for the given maximum K
        Throws exception when that is the case
        """
        #min filtersize
        f = self.filters[0]
        if f > self.filters[1]:
            f = self.filters[1]
        
        if 2*self.maximumK > f:
            raise Exception, "A filter is set too low for this maximum K. filter value: " + str(f) + " maxK: " + str(self.maximumK)

    def train(self):
        topKPairsVector = IntVector()
        runKTSP(self.data, self.numGenes, self.classSizes,self.filters, self.maximumK, self.nleaveout, self.nValidationRuns, topKPairsVector)
        aPair = []
        for i in xrange(len(topKPairsVector)):
            if len(aPair) == 2:
                self.topKPairs.append((aPair[0], aPair[1]))
                aPair = []
            aPair.append(topKPairsVector[i])
        self.topKPairs.append((aPair[0], aPair[1]))
    
    def getMaxScores(self):
        return self.topKPairs

    def addUnclassified(self, unclassifiedVector):
        self.unclassified_data_vector = unclassifiedVector

    def classify(self):
        classification = []
        for pair in self.topKPairs:
            index1 = pair[0]
            index2 = pair[1]
            if( self.unclassified_data_vector[index1] < self.unclassified_data_vector[index2] ):
                classification.append(0)
            elif self.unclassified_data_vector[index1] > self.unclassified_data_vector[index2]:
                classification.append(1)
            else:
                classification.append(.5)#ties, not happy
        sum = reduce(lambda x,y:x+y, classification)
        if 2*sum > len(self.topKPairs):
            return 1
        else:
            return 0

    def crossValidate(self, k=10):
        """
        Runs the C-based cross validation
        K-fold testing of the given data, returns the percent classified correctly.
        """
        return crossValidate(self.data, self.numGenes, self.classSizes,self.filters, self.maximumK, self.nleaveout, self.nValidationRuns, k)

}
