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


class GMTParser:
    """
This class parses a gmt file and returns a dict of geneNetworks -> list(genes)
The GMT file that has been used in testing is 2.biocarta.v2.5.symbols.gmt.
Note in 2.0 we should use pyBabel.
    """
    def __init__(self, file_name):
        self.file = file_name
        self.network = {}
        self.network_info = {}
        self._parseFile()

    def _parseFile(self):
        """
        does what it says
        """
        f = open(self.file, 'r')
        for line in f.readlines():
            line_list = line.rstrip().split('\t')   
            self.network[ line_list[0]] = line_list[2:]
            self.network_info[line_list[0]] = line_list[1]
        f.close()
    def _removeRedundant(self, list, netname):
        """
        for testing
        """
        list.sort()
        newList = []
        prev = None
        for val in list:
            if prev != val:
                newList.append(val)
                prev = val
            else:
                print "match"
                print netname
                print val
        return newList

    def getAllNetworks(self):
        """
        Returns a dictionary with a mapping from gene networks to genes.
        The genes are stored as a list of strings.
        """
        return self.network

    def getNetwork(self, name):
        return self.network[name]



if __name__ == '__main__':
    g = GMTParser("../data/c2.biocarta.v2.5.symbols.gmt")
    temp = g.getAllNetworks()    
     
        
