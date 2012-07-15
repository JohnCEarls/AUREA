"""
Copyright (C) 2011  N.D. Price Lab

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from AUREA.learner import wilcoxon
import math
class ResourceEstimate:
    """
    A class for estimating the number of cycles and amount of memory that is 
    going to be necessary to run a particular algorithm
    ********************************
    http://support.hyperic.com/display/SIGAR/Home
    for getting current memory etc
    ********************************
    """
    GIGAHERTZ = 10**9
    GIGABYTES = 1024**3
    SWAP_PENALTY = 10**6

    def __init__(self, data, class1size, class2size, numGenes, gene_net_size, ram=None, processor_speed=1.0):
        self.ram = ram
        self.processor_speed = processor_speed
        self.data = data
        self.class1size = class1size
        self.class2size = class2size
        self.numGenes = numGenes
        self.wilcoxon = None
        self.gene_net_size = gene_net_size

    def TSPtime(self, restrictions):
        """
        Approximate operations to run TSP
        """
        self._checkRestrictions(restrictions)
        w = self.getWilcoxon()       
        dimensionality = reduce(lambda x,y:x*y , [w.filterAdjust(r) for r in restrictions])
        samp = self.class1size + self.class2size
        return self.wilcoxonTime() + samp*dimensionality

    def TSTtime(self, restrictions):
        """
        Approximate operations to run TST
        """
        w = self.getWilcoxon()       
        dimensionality = reduce(lambda x,y:x*y , [w.filterAdjust(r) for r in restrictions])
        samp = self.class1size + self.class2size
        return samp * dimensionality

    def kTSPtime(self, maxk, num_cross_validate, restrictions):
        """
        Approximate number of operations for kTSP
        """
        samp = self.class1size + self.class2size
        w = self.getWilcoxon()       
        dimensionality = reduce(lambda x,y:x*y , [w.filterAdjust(r) for r in restrictions])
        maxFilter = max([w.filterAdjust(r) for r in restrictions])
        pq_size = 2*maxk*maxFilter

        return self.wilcoxonTime() +  (maxk/2)*(num_cross_validate + 1)*samp*dimensionality + pq_size*math.log(pq_size)
        
    def Diractime(self, min_network_size=3):
        """
        Approximate number of operations for Dirac
        IDM: k
        IRM: k
        grt: s*x
        grms: s*x
        grci: 2*x
        Where x is the sum of n choose 2 where n is the cardinality
            of each gene network for all gene networks
        """
        dimensionality = sum([x*x for x in self.gene_net_size if x >= min_network_size])/2
        samp = self.class1size + self.class2size        
        return (samp + samp + 2) * x

    def TSPspace(self, restrictions):
        w = self.getWilcoxon()       
        dimensionality = reduce(lambda x,y:x*y , [w.filterAdjust(r) for r in restrictions])
        samp = self.class1size + self.class2size
        return dimensionality + samp*self.numGenes

    def TSTspace(self, restrictions):
        w = self.getWilcoxon()       
        dimensionality = reduce(lambda x,y:x*y , [w.filterAdjust(r) for r in restrictions])
        samp = self.class1size + self.class2size
        return dimensionality + samp * self.numGenes


    def kTSPspace(self, maxk, num_cross_validate):
        """
        size(table) + size(input_data) +  size(rank_sum) + 
        """
        samp = self.class1size + self.class2size
        dimensionality = reduce(lambda x,y:x*y , [w.filterAdjust(r) for r in restrictions])
        maxFilter = max([w.filterAdjust(r) for r in restrictions])
        return dimensionality + samp*self.numGenes + 2*maxFilter + 2*maxK*maxFilter
        
    def Diracspace(self):
        """
        IDM: k
        IRM: (s+2)*x bits
        grt: k
        grms: k
        grci = 2*num gene nets
        """
        samp = self.class1size + self.class2size
        x = sum([x*x for x in self.gene_net_size])/2
        
        return (samp + 2)*x/64 + 2* len(self.gene_net_size)

    def wilcoxonTime(self):
        samp = self.class1size + self.class2size
        return samp*self.numGenes*(math.log(self.numGenes) + math.log(samp))

    def getWilcoxon(self):
        """
        Returns a Wilcoxon object
        """
        if self.wilcoxon is None:
            self.wilcoxon = wilcoxon.Wilcoxon(self.data, self.numGenes, self.class1size, self.class2size)
        return self.wilcoxon

    def getSeconds(self, cycles, mem_req):
        sec = cycles/(self.processor_speed * ResourceEstimate.GIGAHERTZ)        
        if self.willSwap(mem_req):
            sec = sec * ResourceEstimate.SWAP_PENALTY  
        return sec

    def willSwap(self, mem_req):
       if self.ram is not None:
             return self.ram * ResourceEstimate.GIGABYTES < mem_req

    def _checkRestrictions(self, restrictions):
        for restriction in restrictions:
            assert restriction < self.numGenes, "Filter is larger than available genes"
   
