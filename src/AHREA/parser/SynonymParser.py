class SynonymParser:
    """
    A parser for gene_info.gs from ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/
    This will may need to be expanded in order to allow other
    sources for synonyms, but this seems pretty comprehensive.
    """
    def __init__(self):
        self.syn = None

    def importgene_info(self, fname):
        """
        A specific function to read the gene_info.gz
        you need to provide with the name and path to gene_info.gz
        see ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/README to see how it is
        layed out
        """
        import gzip
        #import os
        #import os.path
        #fpath = os.path.join("..", "data")
        f = gzip.open(fname, 'rb')
        line = f.readline()
        counter = 0
        graph = {}
        while line:
            myline = line.strip().split('\t')
            if myline[4][0] != '-':
                edgelist = myline[4].split("|")
                edgelist.append(myline[2])
                merge_list = []
                for v in edgelist:
                    if v in graph:                                              
                        merge_list.append(graph[v])                        
                    else:
                        graph[v] = edgelist
                if len(merge_list) > 0:
                    #if a syn is for multiple sets we need to merge them
                    original = merge_list[0]
                    for lists in merge_list[1:]:
                        #more than one merge
                        for val in lists:
                            if val not in original:
                                original.append(val)
                            graph[val] = original
                    for val in edgelist:
                       if val not in original:
                            original.append(val)
                       graph[val] = original
            counter += 1
            line = f.readline()

        f.close()
        self.syn = graph

    def getSynonyms(self, geneName):
        if geneName in self.syn:
            return self.syn[geneName]
        else:
            return None

    def testAll(self):
        """
        For testing
        """
        for gene in self.syn.iterkeys():
            for syns in self.syn[gene]:
                if self.syn[gene] != self.syn[syns]:
                    print "Oh noes!!!!!"
        
if __name__ == "__main__":
    s = SynonymParser()
    s.importgene_info("../data/Homo_sapiens.gene_info.gz")
    #print s.syn
    print s.getSynonyms('CLC4')
    print s.getSynonyms('John Is Awesome')
    print s.getSynonyms('FLJ23393')
    s.testAll()