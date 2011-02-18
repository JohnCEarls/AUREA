import unittest
import SOFTParser
import GMTParser
import DataCleaner
import DataPackager
import dirac

class IncreasingC1DecreasingC2(unittest.TestCase):
    def setUp(self, class1Size=10, class2Size=10, sampleSize=100):
        #create 2 classes, one increasing one decreasing
        self.classVector = dirac.IntVector()
        self.classVector.push_back(class1Size)
        self.classVector.push_back(class2Size)
        self.sampleSize = sampleSize
        self.data = dirac.DoubleVector()
        base_number = 1.0
        
        for x in xrange(self.classVector[0]):
            for y in xrange(self.sampleSize): 
                self.data.push_back(base_number)
                base_number += .5
        if class1Size < class2Size:
            base_number += (class2Size - class1Size) * sampleSize;
        for x in xrange(self.classVector[1]):
            for y in xrange(self.sampleSize):
                self.data.push_back(base_number)
                base_number -= .5

    def test_data_size(self):
        self.assertEqual(len(self.data), (self.classVector[0] + self.classVector[1]) * self.sampleSize, 'data incorrect size')

    def test_class_size(self):
        self.assertTrue(len(self.classVector) == 2, 'wrong number of class vectors')
        self.assertTrue(self.classVector[0] > 0, 'class 1 vector has invalid size')
        self.assertTrue(self.classVector[1] > 0, 'class 2 vector has invalid size')
  

    def test_class1_data(self):
        x=1
        self.assertTrue(self.data[0] > 0, 'class 1 has negative numbers')
 
        while(x < self.classVector[0] * self.sampleSize):
            self.assertTrue(self.data[x-1] < self.data[x], 'class 1 is not increasing')
            self.assertTrue(self.data[x] > 0, 'class 1 has negative numbers')
            x += 1

    def test_class2_data(self):
        x=self.classVector[0] * self.sampleSize
        self.assertTrue(self.data[x] > 0, 'class 2 has negative numbers')
        x +=1
        while(x < (self.classVector[0]+self.classVector[1]) * self.sampleSize):
            self.assertTrue(self.data[x-1] > self.data[x], str(x-1) + " to " + str(x) + ' of class 2 is not decreasing')
            self.assertTrue(self.data[x] > 0, 'class 2 has negative numbers')
            x += 1


def nChooseTwo( n):
    return (n*(n-1))/2
 
class DiracBasicIC1DC2(IncreasingC1DecreasingC2):
    def Internal_setup(self):
        #create geneNetworks of size 20
        self.geneNetwork = dirac.IntVector()
        self.geneNetworkSize = dirac.IntVector()
        self.geneNetworkStart = dirac.IntVector()
        start = 0
        self.geneNetworkStart.push_back(start)
        for x in xrange(self.sampleSize):
            self.geneNetwork.push_back(x)
            if(x % 20 == 0):
                self.geneNetworkSize.push_back(20)
                start += nChooseTwo(20)
                self.geneNetworkStart.push_back(start)
        self.dirac = dirac.Dirac(self.data, self.sampleSize, self.classVector, self.geneNetwork, self.geneNetworkSize, self.geneNetworkStart)
        self.dirac.train()

    def test_gene_network(self):
        self.Internal_setup()
        self.assertTrue( len(self.geneNetwork) == len(self.data)/(self.classVector[0] + self.classVector[1]), 'geneNetworks are not the same size as data');            
        sum = 0
        for x in xrange(len(self.geneNetworkSize)):
            sum += self.geneNetworkSize[x]
        
        self.assertTrue(sum == len(self.geneNetwork),'geneNetwork size ' + str(len(self.geneNetwork))  + ' does not match geneNetworkSize ' + str(sum) )

    def test_rank_matrix(self):
        self.Internal_setup()
        self.assertTrue(len(self.dirac.RankMatrix) > 0, 'Rank matrix is empty')
        rankMatrixColLength = 0
        for x in self.geneNetworkSize:
            rankMatrixColLength += nChooseTwo(x)
        rankMatrixLength = rankMatrixColLength * (self.classVector[0] + self.classVector[1] + 2)    
        self.assertTrue(len(self.dirac.RankMatrix) == rankMatrixLength, 'Rank Matrix does not match expected length')
        #check that the rankMatrices have good values
        counter = 0
        for x in self.dirac.RankMatrix:
            if counter < len(self.dirac.RankMatrix)/2:
                self.assertTrue(x , 'RankMatrix class 1 has bad value')
            else:
                self.assertFalse( x , 'RankMatrix class 2 has bad value')
            counter += 1
        #test rank list
        rankList = self.dirac.getRankMatrix()
        counter = 0
        self.assertTrue(len(rankList) == (self.classVector[0] + self.classVector[1]), 'rankList has the wrong number of columns')
        for list in rankList:
            self.assertTrue(len(list) == rankMatrixColLength, 'The rank list columns have a bad length')
            for val in list:
                if counter < self.classVector[0]:
                    self.assertTrue(val, 'Rank List has bad class 1 value')
                else:
                    self.assertFalse(val, 'Rank List has bad class 2 value')
            counter += 1
    
    def test_rank_template(self):
        self.Internal_setup()
        rankMatrixColLength = 0
        for x in self.geneNetworkSize:
            rankMatrixColLength += nChooseTwo(x)

        rankTemplates = self.dirac.getRankTemplates()
        self.assertTrue(len(rankTemplates) == 2, 'incorrect number of rankTemplates')
        self.assertTrue(2*rankMatrixColLength == (len(rankTemplates[0])+len(rankTemplates[1])), 'rank templates have incorrect length')
        for val in rankTemplates[0]:
            self.assertTrue(val, 'Incorrect rankTemplate value for class 1')
        for val in rankTemplates[1]:
            self.assertFalse(val, 'Incorrect rankTemplate value for class 2')

    def test_Rank_Conservation(self):
        self.Internal_setup()
        rankCon = self.dirac.getRankConservation()
        self.assertTrue(len(rankCon) == len(self.geneNetworkSize), 'RankConservation list has incorrect number of elements')
        for netRankCon in rankCon:
            self.assertTrue(netRankCon[0] == netRankCon[1], 'rank conservation values are bad')

    def test_rank_difference(self):
        self.Internal_setup()
        rd = self.dirac.getRankDifference()
        for x in rd:
            self.assertFalse(x[0] > 0.001, 'rank Difference is wrong')
    
    def test_class1_unclassified(self):
        self.Internal_setup()
        self.unclassified = dirac.DoubleVector()
        base_number = 1.0
        for y in xrange(self.sampleSize):
            self.unclassified.push_back(base_number)
            base_number += .5
        self.dirac.addUnclassified(self.unclassified)
        classification = self.dirac.classify()
        self.assertTrue( classification[0][0] == 0, 'Improperly Classified' )
        self.assertTrue( classification[0][1] > .99999, 'Bad matching score on class 1 = ' +  str(classification[0][1]))
        self.assertTrue( classification[0][2] < .01, 'Bad matching score on class 2')
 
    def test_class2_unclassified(self):
        self.Internal_setup()
        self.unclassified = dirac.DoubleVector()
        base_number = 1000.0
        for y in xrange(self.sampleSize):
            self.unclassified.push_back(base_number)
            base_number -= .5
        self.dirac.addUnclassified(self.unclassified)
        classification = self.dirac.classify()
        self.assertTrue( classification[0][0] == 1, 'Improperly Classified' + str(classification[0]) )
        self.assertTrue( classification[0][1] < .99999, 'Bad matching score on class 1 = ' +  str(classification[0][1]))
        self.assertTrue( classification[0][2] > .01, 'Bad matching score on class 2')
    def test_data(self):
        self.assertTrue(len(self.data) > 0, 'Data is not null')

if __name__ == '__main__':
    unittest.main()
    """
    suite1 = IC1DC2suite()
    suite2 = DBsuite()
    alltests = unittest.TestSuite([suite1, suite2])
    result = unittest.TestResult()
    alltests.run(result)
    if(not result.wasSuccessful()):
       for fail in result.failures:
            print "-"*40
            print fail[0]
            print 
            print fail[1]
    else:
        print "All tests passed"
    """
