%pythoncode{
class KTSP:
    def __init__(self, data, numGenes, classSizes, filters, maximumK, nleaveout, nValidationRuns):
        """
        Creates a ktsp learner object
            data - DoubleVector with data
            numgenes - number of genes per sample
            classSizes = IntVector of size 2 where a[0] = class 1 size
            filters - IntVector of size 2 used for wilcoxon filtering
            maximumK - largest k to search against (running time increases linearly on this k)
            nleaveout - number of samples to leave out on cross validation for finding optimal k
            nValidationRuns - number of times to run cross validation for finding optimal k
        """
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
        """
        Trains the object
        """
        topKPairsVector = IntVector()
        runKTSP(self.data, self.numGenes, self.classSizes,self.filters, self.maximumK, self.nleaveout, self.nValidationRuns, topKPairsVector)
        aPair = []
        for i in xrange(len(topKPairsVector)):
            if len(aPair) == 2:
                self.topKPairs.append((aPair[1], aPair[0]))
                aPair = []
            aPair.append(topKPairsVector[i])
        self.topKPairs.append((aPair[1], aPair[0]))
    
    def getMaxScores(self):
        """
        Get a list of tuples containing the chosen pairs
        """
        return self.topKPairs

    def addUnclassified(self, unclassifiedVector):
        """
        Adds an unclassified vector for classification
        """
        self.unclassified_data_vector = unclassifiedVector

    def classify(self):
        """
        classifies vector provided by addUnclassified method
        """
        classification = []
        for pair in self.topKPairs:
            index1 = pair[0]
            index2 = pair[1]
            if( self.unclassified_data_vector[index1] > self.unclassified_data_vector[index2] ):
                classification.append(0)
            elif self.unclassified_data_vector[index1] < self.unclassified_data_vector[index2]:
                classification.append(1)
            else:
                classification.append(.5)#ties, not happy
        sum = reduce(lambda x,y:x+y, classification)
        if 2*sum > len(self.topKPairs):
            return 1
        else:
            return 0

    def crossValidate(self, k=10, use_acc=True):
        """
        Runs the C-based cross validation
        K-fold testing of the given data, returns the percent classified correctly if use_acc true, MCC if false
        """
        return crossValidate(self.data, self.numGenes, self.classSizes,self.filters, self.maximumK, self.nleaveout, self.nValidationRuns, k, use_acc)

}
