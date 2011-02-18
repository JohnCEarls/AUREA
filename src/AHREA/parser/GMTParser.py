
class GMTParser:
    """
This class parses a gmt file and returns a dict of geneNetworks -> list(genes)
    """
    def __init__(self, file_name):
        self.file = file_name
        self.network = {}
        self.network_info = {}
        self.parseFile()

    def parseFile(self):
        f = open(self.file, 'r')
        for line in f.readlines():
            line_list = line.rstrip().split('\t')   
            self.network[ line_list[0]] = line_list[2:]
            self.network_info[line_list[0]] = line_list[1]
        f.close()
    def removeRedundant(self, list, netname):
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
        return self.network

    def getNetwork(self, name):
        return self.network[name]



if __name__ == '__main__':
    g = GMTParser("../data/c2.biocarta.v2.5.symbols.gmt")
    temp = g.getAllNetworks()    
     
        
