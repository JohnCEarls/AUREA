%pythoncode{
class Wilcoxon:
    def __init__(self, data, numGenes, class_1_size, class_2_size):
        scores_vector = DoubleVector()
        for x in range(0,numGenes):
            scores_vector.push_back(0.0)
        runWilcoxonTest(data, numGenes, class_1_size, class_2_size, scores_vector)
        self.scores = [x for x in scores_vector]
        self.sorted =None 
        self.cheat =len(self.scores) -1 

    def getScores(self):
        return self.scores

    def filterAdjust(self, filter):
        """
        This function takes an integer and determines how many wilcoxon scores
        are the same as the filterth element
        In TSP and TST this acts as an adjustment to the number of genes that are
        considered        
        """
        if self.sorted is None:
            self.sorted = sorted(self.scores, reverse=True)
        val = self.sorted[filter]
        counter = filter
        if self.sorted[self.cheat] == val and counter < self.cheat:
            counter = self.cheat
             
        n = len(self.sorted)
        while counter < n and val == self.sorted[counter]:
            counter += 1
        self.cheat = counter -1
        return counter-1
}
