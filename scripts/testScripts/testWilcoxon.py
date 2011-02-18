from learner import wilcoxon
import random
if __name__ == "__main__":
    vals = []
    import math
    import scipy.stats
    for x in range(1):
        ngenes = 10
        n_c1 = 80
        n_c2 = 18

        data = wilcoxon.DoubleVector()
        start = 1000.05
        for x in range(0, n_c1):
            for y in range(0,ngenes):
                data.push_back(start)
                start -= .01
        for x in range(0, n_c2):
            for y in range(0,ngenes):
                data.push_back(start)
                start += .01
            
        W = wilcoxon.Wilcoxon(data, ngenes, n_c1, n_c2)
        print W.getScores()
        s= [1 for x in range(180)]
        z = [19 for x in range(180)]
        print scipy.stats.mannwhitneyu(s,z)
        
    
    

     
