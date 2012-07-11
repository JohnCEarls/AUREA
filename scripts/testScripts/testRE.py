from learner import ktsp, tst, dirac, tsp
from parser import SOFTParser, GMTParser
from adaptive import ResourceEstimate
from adaptive import LearnerQueue
import random
from testScripts import testTemplate

def getScores(learner):
    myfile = open('test' + str(learner) + '.csv')
    temp = []
    for line in myfile.readlines():
        cur = line.strip().split('~')
        if len(cur) > 1:
            time = cur[2]
            for val in cur:
                if val[0] == '[':
                    netsize = val[1:-1]
                    netsize = netsize.split(',')
            temp.append((time, netsize))
        myfile.close()
    return temp 
def testTSP():
    a = getScores(1)
    d = []
    for x in a:
        if (int(x[1][0]) < int(x[1][1])):
            print "="*20
            print x[0]
            print int(x[1][0]) * int(x[1][1])
            print (int(x[1][0]) - int(x[1][1]))**2
            d.append((int(x[1][0])**2,float(x[0]),int(x[1][0]), int(x[1][1]))) 
    d.sort()
    for x in d:
        print x 

               
dp = testTemplate.getDataPackage()
#print "got dp"
lq = LearnerQueue.LearnerQueue(dp)
min_net_size = (10, 3, -1)
numTop = (1,5,1)
lq.genDirac(min_net_size, numTop)
r1 = (10, 700, 10)
r2 = (10, 700, 10)
lq.genTSP(r1, r2)
r1 = (10, 100, 10)
r2 = (10, 100, 10)
r3 = (10, 100, 10)
lq.genTST(r1, r2, r3)
r1 = (40, 1000, 50)
r2 = (40, 1000, 50)
k = (10, 21, 5) 
ncv = (1, 2)
nlo = (0, 1)
lq.genKTSP(k,ncv,nlo, r1, r2)
ran = []
import time 
counter = 1
viewable = ['dirac', 'tsp', 'tst', 'ktsp']
for est, settings in lq:   
    if settings['learner'] > -1 : 
        print "+"*10
        print viewable[settings['learner']]
        print "Est: ",
        print est
        print "Scale: ",
        print lq.scale[settings['learner']]
        print "Weight: ",
        print lq.weight[settings['learner']]
        print "Adj Score: ",
        print est/( lq.scale[settings['learner']] * lq.weight[settings['learner']])
        print "Time Est.: ",
        print  est/lq.scale[settings['learner']]

        rest = []
        if 'restrictions' in settings:
            rest = [x for x in settings['restrictions']]
        boring_settings = ['data', 'numGenes', 'restrictions']
        print " "*3,
        print "restrictions: ",
        print rest
        unboring = [k for k in settings.keys() if k not in boring_settings]
        for k in unboring:
            print " "*3,
            print k + ": ",
            print settings[k]
        
        learner = lq.trainLearner(settings, est)
        cv = learner.crossValidate()
        lq._adjWeight(settings['learner'], cv)
        print "Acc:",
        print cv
        print "-"*20
        print lq.weight
        if cv > .98:
            print "Good enough"
            exit()
        
