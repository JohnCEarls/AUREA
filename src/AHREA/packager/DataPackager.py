from AUREA.learner import dirac
import pyBabel.Extensions
class dataPackager:
    """
This class takes a set of data tables and generates data vectors and class vectors (and geneNet vectors if wanted) suitable for processing by the algorithms.
    """
    def __init__(self, merge_cache='data'):
        self.data_tables = []
        self.classifications = []
        self.gene_networks = {}
        self.synonyms = None
        self.class_vector = None
        self.gene_data_vector = None
        self.probe_data_vector = None
        self.gene_net_vector = None
        self.gene_net_size_vector = None
        self.gene_index = None
        self.probe_index = None
        self.genes = None
        self.probes = None
        self.unclassified = None
        self.unclassified_data_vector = None
        self.merge_cache = merge_cache

    def setMergeCache(self, cache_dir): 
        """
This is for setting the directory that stores cached merge-tables.
This value is passed to pyBabel.
        """
        self.merge_cache = cache_dir

    def getDataVector(self, type):
        """
This generates a tuple containing (a vector of floats, the size of the columns(number of genes/probes in this context.
It uses the dirac library to form the floatVector.
        """
        numSamples = 0
        class_vector = self.getClassVector()
        for i in xrange(len(class_vector)):
            numSamples += class_vector[i]
        if self.probe_data_vector == None:
            self.createDataVector()
        if type == 'probe':
            dv = self.probe_data_vector
        elif type == 'gene':
            dv = self.gene_data_vector
        else:
            raise Exception, "Invalid row key given"
        
        if dv:
            return (dv, len(dv)/numSamples)
        else:               
            self.createDataVector()
            if len(dv) % numSamples:
                #check if something screwy went on with our data table
                Exception, "The data vector is malformed: length: " + str(len(dv)) + " number of samples: " + numSamples
            return (dv, len(dv)/numSamples)


    def getGeneNetVector(self, minNumberGenes = 3):
        """
This returns a tuple containing (genelocations relative to data vector in intVector, numgenes in each set in intVector format).
        """
        if self.gene_net_vector:
            return (self.gene_net_vector,self.gene_net_size_vector) 
        else:
            self.createGeneNetVector(minNumberGenes) 
            return (self.gene_net_vector, self.gene_net_size_vector) 

    def getGeneNetName(self, geneNetIndex):
        """
Given the index into the geneNetwork array, return the human readable name of the network.
        """
        return self.gene_net_map[geneNetIndex]
    
    def getGeneName(self, index, type='gene'):
        """
Given an index into either the probe or gene array(determined by the type parameter,) return the human readable name of the probe/gene.
        """
        if type=='gene':
            return self.genes[index]
        else:
            return self.getGeneNameFromProbeName(self.getProbeName(index)) + '-'+ self.getProbeName(index)
    
    def getProbeName(self, probe_index, tbl_indx=0):
        if isinstance(self.probes[probe_index], tuple):
            #merged probe, so join names
            return self.probes[probe_index][tbl_indx]
           
        return self.probes[probe_index]

    def getGeneNameFromProbeName(self, probe_name, dt_indx=0):
        """
        Given a probe name
        return the gene name
        """
        #not storing it here so we have to go back to the data tables
        dt1 = self.data_tables[dt_indx]
        return dt1.genes[dt1.probe_index[probe_name]]
        

    def getClassVector(self):
        """
        This returns an intVector with the number of genes in each class.  This should map to columns in the dataVector, for example a vector containing (4,5,8) means that the first class is the first 4 columns, the second class is the 5th-8th column, etc.)  Bear in mind I'm a programmer and count from zero. 
        """
        if self.class_vector:
            return self.class_vector
        else:
            self.createClassVector()
            return self.class_vector

    def addDataTable(self, dataTable):
        """
        This adds a set of tables from which we will create our data vector.
        The tables should come from DataTable class.
        Data table names are accessible through dataTable.dt_id
        """
        self.data_tables.append( dataTable )
        self.genes = None

    def clearUnclassified(self):
        """
        Clears out data relating to an 
        unclassified sample (sample to be classified)
        """
        self.unclassified = None
        self.unclassified_data_vector = None
    def clearClassification(self):
        """
        Clears the classification settings
        """
        self.classifications = []
        self.class_vector = None 
        self.clearData()

    def clearClassSamples(self):
        """
        Removes the samples from the classifications list
        """
        for className, samples in self.classifications:
            samples = []

    def clearData(self):
        """
        Clears the gene and probe data vectors
        """
        self.probe_data_vector = None
        self.gene_data_vector = None
        
    def createClassification(self, className):
        """
        This creates a new class we can add samples to that is identified by the string provided as className
        """
        self.classifications.append((className, []))


    def addToClassification(self, classToAddTo, data_table, sample):
        """
        Adds a sample to a class.
        classToAddTo (string) is a string that was added with createClassification.
        data_table (string) is the dt_id from a DataTable object
        sample (string) is the name of the sample to be added.
        """
        for className, samples in self.classifications:
            if classToAddTo == className:
                samples.append( (data_table, sample) )            
   
    def getClassifications(self):
        """
        Returns the set of classifications we are training on
        organized as
        [(className1, [ (table, sample_id), (table, sample_id) ...]),
         (className2, [ (table, sample_id), (table, sample_id) ...])]
         
        """
        return self.classifications

    def createUnclassifiedDataVector(self, type):
        """
        This takes the unclassified data list and converts it to a vector 
        of doubles.
        type is gene/probe
        """
        self.unclassified_data_vector = None
        self.unclassified_data_vector = dirac.DoubleVector()
        prevTable = None
        t_obj = self.getTable(self.unclassified[0])
        for i, t in enumerate(self.data_tables):
            if t==t_obj:
                t_indx = i
        sample = self.unclassified[1]
        if type=='probe':
            for p in self.probes:
                if isinstance(p, tuple):
                    p = p[t_indx]
                self.unclassified_data_vector.push_back( t_obj.getData(sample, probe_name=p) )
        else:
            for g in self.genes:
                self.unclassified_data_vector.push_back( t_obj.getData(sample, gene_name=g) )
 

    def getUnclassifiedDataVector(self, type):
        self.createUnclassifiedDataVector(type)
        return self.unclassified_data_vector
        
    def setUnclassified(self, data_table, sample):
        """
        Create unclassified tuple containing table and sample name
        """
        self.unclassified = (data_table, sample)

    def addGeneNetwork(self, geneNetwork):
        """
        Adds a gene network object.
        """
        for name, genes in geneNetwork.iteritems():
            if name not in self.gene_networks:
                self.gene_networks[name] = genes
            else:
                for gene in genes:
                    self.gene_networks[name].append(gene)
        
    
    def createDataVector(self):
        """
        Builds the probe and gene data vectors
        """
        if len(self.data_tables) == 0:
            raise Exception("Attempt to create a data vector without a data table")
        if self.genes == None:
            self.mergeTables()
        self.createProbeDataVector()
        self.createGeneDataVector()

    def buildDataVector(self, type):
        """
        This builds the data vector from the given information
        """
        if type == 'gene':
            dv = self.gene_data_vector = dirac.DoubleVector()
            row_list = self.genes
            parameter_index = 1
        else:#probe
            dv = self.probe_data_vector = dirac.DoubleVector()
            row_list = self.probes
            parameter_index = 2
        prevTable = None
        #for each class
        for classification, samples in self.classifications:
            #for each sample in class
            for table, sample in samples:
                #for each gene in sample in class
                if prevTable != table:
                    t_obj = self.getTable(table)
                    for i, t in enumerate(self.data_tables):
                         if t==t_obj:
                            t_indx = i
                    prevTable = table
                #base parameter template
                param = [sample, None, None]
                for name in row_list:
                    if isinstance(name,tuple):#merged data, find probe name for this table
                        param[parameter_index] = name[t_indx]
                    else:
                        param[parameter_index] = name
                    T = tuple(param)
                    dv.push_back( t_obj.getData(*T ) )#passing in parameter tuple

    def createProbeDataVector(self):
        """
        creates self.probe_data_vector
        """
        self.buildDataVector('probe')

    def createGeneDataVector(self):
        """
        Creates self.gene_data_vector
        """
        self.buildDataVector('gene')

    def createClassVector(self):
        """
Goes through the classification vector and puts the classSize in the order they
will be presented in the data vector
        """
        self.class_vector = dirac.IntVector()
        for className, samples in self.classifications:
            self.class_vector.push_back( len(samples) )

    def createGeneNetVector(self, minNetSize = 10):
        """
This builds the geneNet Vector from the provided information.  It uses gene synonyms if available
        """
        self.gene_net_vector = dirac.IntVector()
        self.gene_net_size_vector = dirac.IntVector()
        self.gene_net_map = []#a list of the geneNetNames in the order they are sent to Dirac        
        self.gene_net_data_matrix_start = []
        dmstart_counter = 0
        for net_name, network in self.gene_networks.iteritems():#4each net
            network_size_counter = 0#since not all genes in network are in data
            for gene in network:#4each gene in net
                if gene in self.gene_index:#if the gene is in our data
                    row_number = self.gene_index[gene]
                    self.gene_net_vector.push_back(row_number)
                    network_size_counter += 1
                elif self.synonyms:
                    #look for synonym
                    ourSyn = self.synonyms.getSynonyms(gene)
                    if ourSyn:
                        for syngene in ourSyn:#go through the synonyms for the gene
                            if syngene in self.gene_index:
                                #we found a match in the index so add it
                                row_number = self.gene_index[syngene]
                                self.gene_net_vector.push_back(row_number)
                                network_size_counter += 1
                                break 
             
            if network_size_counter > minNetSize:
                self.gene_net_size_vector.push_back( network_size_counter )
                self.gene_net_map.append(net_name)
                self.gene_net_data_matrix_start.append(dmstart_counter)
                dmstart_counter += (network_size_counter*(network_size_counter -1))/2
            else:
                #the network is too small so remove the genes we added
                while network_size_counter > 0:
                    self.gene_net_vector.pop_back()
                    network_size_counter -= 1
        self.gene_net_data_matrix_start.append(dmstart_counter)

    def mergeTables(self):
        """
        This function merges the gene lookup tables
        """
        pB = pyBabel.Extensions.ext(cache_dir=self.merge_cache)
        try:
            self.probes = pB.mergeProbes(idLists=[table.probes for table in self.data_tables])
        except pyBabel.Extensions.pyBabelError, E:#unable to merge on probes
            print E.value            
            self.probes = [] 
        
        self.probe_index = {}
        for i, probeset in enumerate(self.probes):
            self.probe_index[probeset] = i
        
        geneset = set(self.data_tables[0].genes)
        if len(self.data_tables) > 1:
            for table in self.data_tables[1:]:
                geneset.intersection_update(table.genes)

        self.genes = [x for x in geneset]
        self.gene_index = {}

        for i, gene in enumerate(self.genes):
            self.gene_index[gene] = i

    def getDataCount(self):
        """
        Returns a tuple with
        (num genes in merge, numprobes in merge)
        """
        numgenes = len(self.genes)
        numprobes = len(self.probes)
        return (numgenes, numprobes)
           
    def getGeneNetCount(self):
        if self.gene_networks is not None and len(self.gene_networks) > 0:
            self.createGeneNetVector(1)
            numnetworks = len(self.gene_net_size_vector)
            if numnetworks > 0:
                min = 10000
                max = 0
                sum = 0
                for geneset in self.gene_net_size_vector:
                    if geneset > max:
                        max = geneset
                    if geneset < min:
                        min = geneset
                    sum += geneset
                ave = float(sum)/numnetworks
            else:
                min = None
                max = None
                ave = None        
            
            return (numnetworks, ave, max, min)
        return None

    def getGeneNetVectorRange(self, net_number):
        """
        Returns the start and number of elements in the 
        """
        s = self.gene_net_data_matrix_start[net_number]
        e = self.gene_net_data_matrix_start[net_number+1]
        return (s,e)
                    
  
    def getGeneNetDataMatrixStart(self):
        """
        Returns a list that details where in the data matrices a given
        gene network starts and stops (based on size nchoose2)
        """
        return self.gene_net_data_matrix_start
 
    def addSynonyms(self, file):
        """
Adds a table of synonyms to allow cross referencing between geneNets and datasets.
        """
        import AUREA.parser.SynonymParser as sp
        self.synonyms = sp.SynonymParser()
        self.synonyms.importgene_info(file)

    def getTables(self):
        """
        Returns list of data_table objects
        """
        return self.data_tables

    def getTable(self, table_id):
        """
        Returns table object that has that table_id
        """
        for table in self.data_tables:
            if table.dt_id == table_id:
                return table

    def writeToCSV(self, filename, key='gene'):
        """
        Writes the current data from your chosen classes to csv format.
        With given key (gene/probe)
        Note: you must provide a valid path and filename to this function

        Thats on you        
        """
        csv_file = open(filename, 'w')
        csv_file.write(self._getCSVHeader(key) + '\n')
        dv, numGenes = self.getDataVector(type=key)
        numSamples = len(dv) /numGenes
        for i in range(numGenes):
            str_buff = "'" 
            str_buff += self.getGeneName(index = i, type=key)
            str_buff += "'"
            for j in range(numSamples):
                dv_index = j*numGenes + i
                str_buff += ","
                str_buff += str(dv[dv_index])
            csv_file.write( str_buff + '\n') 
        csv_file.close()
       
    def _getCSVHeader(self, key='gene'):
        """
        Creates the header row for writeToCSV
        """
        classifications = self.getClassifications()
        if len(classifications) == 0:
            raise Exception, "You must add data to classes to print a CSV" 
        c1name, c1samples = classifications[0]
        c2name, c2samples = classifications[1]
        numColumns = len(c1samples)
        header = "'" 
        header += key 
        for s1heading in [table + "." + sample for table, sample in c1samples]:
            header += "','" + s1heading
        for s2heading in [table + "." + sample for table, sample in c2samples]:
            header += "','" + s2heading
        return header + "'"

