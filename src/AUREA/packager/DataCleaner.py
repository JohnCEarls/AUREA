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

import os.path
import copy, re, yaml
from GEO.Sample import Sample
from warn import *

class DataTable:
    """
    This is the representation of a data table.
    """
    def __init__(self, probe_column='ID_REF', gene_column='IDENTIFIER', 
                 gene_collision_rule = 'MAX', bad_data = 0.0, max_bad_cell_percentage=.5):
        """
        gene_collision_rule = determines how we merge genes with multiple entries ('MAX','MIN','AVE' or None)
        bad_data = the default value for bad data cells
        max_bad_cell_percentage = is the percentage of cells in a column/sample that can be bad before we remove the column
        """
        self.dt_id = None #this is a unique name for this data table
        self.sp = None #if this data table is generated by a SOFTParse, this points at the original SOFTParse object, note this is set to None after read
        self.genes = None       # victor: list of gene names (?)
        self.probes = None      # victor: list of probes (?)
        self.samples = None     # victor: list of column headings from soft file (ie, sample names)
        self.sample_description = {}
        self.gene_index = None  # victor: gene->index mapping
        self.probe_index = None # victor: probe->index mapping
        self.sample_index = {}  # victor: sample->index mapping
        self.collision_rule = gene_collision_rule
        self.purged_rows = []
        self.purged_columns = []
        self.string_column_limit = max_bad_cell_percentage #allow 50% bad column
        self.bad_data = bad_data #default value for bad data
        #the headings of the probe and gene columns
        self.probe_column = probe_column
        self.gene_column = gene_column
        self.subsets = []
        # victor: data (matrix) is stored in self.data_table (not mentioned here in __init__)

    def getSOFTData(self, SOFTParse, tableNumber = 0):
        """
        takes a softparse object and turns it into a DataTable object
        """
            
        self.sp = SOFTParse
        #name the data table after its data source
        fn = os.path.split(self.sp.filename)[1]
        self.dt_id = fn + "_table_" + str(tableNumber)
        self.samples = copy.deepcopy(self.sp.getColumnHeadings())
        for c_name, c_description in self.sp.getColumnHeadingsInfo():
            self.sample_description[c_name] = copy.deepcopy(c_description)
        rhset = False
        self.genes = copy.deepcopy( self.sp.getIDENTIFIER(self.gene_column, tableNumber) )
        self.probes = copy.deepcopy( self.sp.getID_REF(self.probe_column ) )
        #deepcopy cost 10 seconds.
        #see if this causes problems
        self.data_table = self.sp.getTable(lock=True) 

        self.cleanUp()
        #subset definition
        #truth be told I am really worried about this
        #dont really have time to test it
        sstemp = self.sp.getSubsets()
        for ssentity in sstemp: # victor: entities are _______ ?
            if 'subset_sample_id' in ssentity.attributes and len(ssentity.attributes['subset_sample_id']) != 0:
                ss_samples = ssentity.attributes['subset_sample_id'][0].split(',')
                ss_desc =  ssentity.attributes['subset_description'][0]

                self.subsets.append( (ss_desc, ss_samples) )            
        self.sp = None #so garbage collection can pick it up

    def getCSVData(self, CSVParse):
        """
        Takes a CSVParser object and turns it into a DataTable object
        """
        self.probe_column =CSVParse.probe_column_name
        self.gene_column = CSVParse.gene_column_name
        self.csv = CSVParse
        fn = os.path.split(self.csv.filename)[1]
        self.dt_id = fn + "_table"
        
        self.samples = copy.deepcopy( self.csv.getColumnHeadings() )
        for c_name, c_description in self.csv.getColumnHeadingsInfo():
            self.sample_description[c_name] = copy.deepcopy(c_description)
        rhset = False
        counter = 0
        self.genes = copy.deepcopy( self.csv.getIDENTIFIER() )
        self.probes = copy.deepcopy( self.csv.getID_REF() )
        #deepcopy cost 10 seconds.
        #see if this causes problems
        self.data_table = self.csv.getTable(lock=True) 

        self.cleanUp()
        self.csv = None #so garbage collection can pick it up


    def getGEOData(self, geoDD):

	# need to set:
	# self.dt_id
	# self.samples (list of sample names)
	# self.sample_descriptions (list of sample descriptions, each of which might be a list of lines)
	# self.genes (ordered list of gene names)
	# self.probes (ordered list of probe names)
	# self.data_table (2D data matrix: [gene/probe index][sample_index]
        #      
	# self.subsets (as necessary) (subsets set but not used by DataTable, others might access)
        pass
            


    def writeAsCSV(self, file):
        """
        Writes the table to a comma separated file
        """
        outfile = open(file, 'w')
        header = "'IDENTIFIER', 'ID_REF'"
        
        for samp in self.samples:
            header += ", '" + samp + "'"
        outfile.write(header +'\r\n')
        
        for i in range(len(self.genes)):
            line = "'"
            line +=self.genes[i] + "', '"
            line +=self.probes[i] + "'"
            for j in range(len(self.samples)):
                line += ", " + str(self.data_table[i][j]) 
            outfile.write(line + '\r\n')

        outfile.close()

    def cleanUp(self):
        """
        Lotso housekeeping
        gets rid of id columns, bad columns, the control rows, 
        converts nulls to given bad data value  
        And builds our indices        
        """
        id_list = []
        #note an error will be thrown if value not in list
        id_list.append( self.samples.index(self.probe_column) )
        id_list.append( self.samples.index(self.gene_column) )
        if id_list[0] == id_list[1]:
            #im thinking that is one or the other is not in there
            #then u could just set both probe and gene col equal
            #but we have to remove one of them in that case
            id_list.pop()
        self.deleteColumn(id_list) #getting rid of id_ref, id ...
        self.loseControl()
        self.loseStringColumns()
        self.makeNumeric()
        #DIRAC goes by geneName while TSP ... goes by probes
        self.handleCollisions( )

        self.purgeRows()
        self.purgeColumns() #gets rid of columns that don't have enough good values
        self.buildGeneIndex()
        self.buildProbeIndex()
        self.buildSampleIndex()
 
    def deleteGene(self, gene_name, buildIndex=True):
        """
        given a gene_name, delete it.
        """
        deleteRow(self.gene_index[gene_name])
        #must rebuild gene_index from this genes location forward
        if buildIndex:
            self.buildGeneIndex(self.gene_index[gene_name])
        del self.gene_index[gene_name]

    def deleteSample(self, sample_name):
        """
        given a sample name, delete the column
        """
        deleteColumn(self.samples[sample_name])
        self.buildSampleIndex(self.samples[sample_name])
        del self.samples[sample_name]

    def loseControl(self):
        """
        Adds any control rows to purge_rows
        """
        counter = 0
        import re
        myre = re.compile('ontrol', flags=re.I)
        
        for heading in self.genes:
            if myre.search(heading) is not None:
               self.purged_rows.append(counter)
            counter += 1

    def purgeRows(self):
        """
        Deletes rows in the purged_rows list
        Should really only be controls
        """
        self.purged_rows.sort(reverse = True)
        prev_row = -1
        for row in self.purged_rows:
            if row != prev_row:
                self.deleteRow(row)
            prev_row = row

    

    def deleteRow(self, index):
        """
        Deletes the row at the given index from the table, genes and probes
        """
        del self.data_table[index]
        del self.genes[index]
        del self.probes[index]
            
    def loseStringColumns(self):
        """
        Checks a column to see if the percent of strings in it is above
        the string_column limit
        If so it adds the column to the purge_columns list and
        this column is deleted in purgeColumns
        """
        columnStringCounter = []
        
        for val in self.samples:
            columnStringCounter.append(0)      
        
        for row in self.data_table:
            counter = 0
            for col in row:
                if not self.isNum(col):
                    columnStringCounter[counter] += 1
                counter += 1
        col_num = 0
        for val in columnStringCounter:
            if val/len(self.genes) > self.string_column_limit:
                self.purged_columns.append(col_num)
            col_num += 1

    def purgeColumns(self):
        """
        Goes through the columns in purged_columns list and deletes them
        """
        self.purged_columns.sort(reverse = True)
        prev_col = -1
        pc = []
        for column in self.purged_columns:
            if column != prev_col:
                pc.append(column)
            prev_col = column
        self.deleteColumn(pc)

    def deleteColumn(self, index):
        """
        Given a list of indices, delete them
        """
        index.sort(reverse=True)
        for row in self.data_table:
            for i in index:
                del row[i]
        for i in index:
            del self.samples[i]
                
    def hasCollisions(self):
        """
        Checks if there exist multiple rows for a single key
        """
        hasCollision = False
        temp = {}
        for gene in self.genes:
            if gene in temp:
                hasCollision = True
                break
            else:
                temp[gene] = 1
        return hasCollision
            
        

    def handleCollisions(self):
        """
        Appends rows to table with data transformation given by collision rule
        applied to that row.
        It also appends the row indices that need to be purged to the purge_rows list
        """
        temp = {}
        row_counter = 0
        for gene in self.genes:
            if gene not in temp:
                temp[gene] = [row_counter]
            else:
                temp[gene].append(row_counter)
            row_counter += 1 
        for key in temp.iterkeys():
            if len(temp[key]) > 1:            
                #creates a new row based on collision rule
                new_row = self.merge_rows(temp[key], self.data_table)
                self.data_table.append(new_row)
                self.genes.append(key)
                self.probes.append(self.collision_rule)
    
    def merge_rows(self, rows, data_table):
        """
        returns a new list that applies the collision rule to the relevant rows
        """
        #NOTE: any changes or additions to this need to be reflected
        #      in packager.DataPackager.dataPackager.mergeTables
        #      just search for dumb
        new_row = []
        for col in xrange(0,len(data_table[0])):#foreach col
            new_row.append(None)#default value that will be changed to bad data value by make numeric
            if self.isNum(data_table[rows[0]][col]):
                if self.collision_rule == 'MAX':
                    for row in rows:
                        if new_row[col] == None or data_table[row][col] > new_row[col]:
                            new_row[col] = data_table[row][col]
                            
                        
                if self.collision_rule == 'MIN':
                    for row in rows:
                        if new_row[col] == None or data_table[row][col] < new_row[col]:
                            new_row[col] = data_table[row][col]
                       
                if self.collision_rule == 'AVE':
                    new_row[-1] = 0.0
                    for row in rows:
                        new_row[col] += float(data_table[row][col])
                    new_row[col] = new_row[col]/len(rows)
            else:
                new_row[col] = data_table[rows[0]][col]
                
        return new_row

    def getNumGenes(self):
        """
        Returns the number of distinct genes
        """
        try: return len(set(self.genes))
        except: return 0

    def getNumProbes(self):
        """
        Returns the number of distinct probes
        """
        try: return len(self.probes)
        except: return 0

    def makeNumeric(self):
        """
        If an element has a bad value(cant make it numeric, this puts the bad value in the spot
        """
        row_index = 0
        for row in self.data_table:
            col_index = 0
            for column in row:
                try:
                    self.data_table[row_index][col_index] = float(column)
                except ValueError:
                    self.data_table[row_index][col_index] = self.bad_data
                col_index += 1
            row_index += 1

    def printDataTable(self):
        """
        Cheap function that prints the datatable to stdout
        """
        for row in self.data_table:
            print row

    def isNum(self, value):
        """
        Returns True if value can be treated as a numeric, false otherwise
        """
        try:
            float(value)
            return True
        except ValueError:
            return False

    def buildSampleIndex(self, start = 0):
        """
        Creates or modifies sample_index
        """
        if self.sample_index == None:
            self.sample_index = {}
        counter = start
        for samp in self.samples[start:]:
            self.sample_index[samp] = counter
            counter += 1

    def buildGeneIndex(self, start = 0):
        """
        Creates or modifies gene_index
        Note that this index points to the merged gene where relevant
        """
        if self.gene_index is None:
            self.gene_index = {}
        counter = start
        #note that the last occurrence of a gene will be the index stored
        #this is the alternative to deleting rows
        for gene in self.genes[start:]:
            self.gene_index[gene] = counter
            counter += 1
    
    def buildProbeIndex(self, start=0):
        """
        Creates or modifies probe index
        """
        if self.probe_index is None:
            self.probe_index = {}
        counter = start
        for probe in self.probes[start:]:
            self.probe_index[probe] = counter
            counter += 1


    def getSamples(self):
        """
        Returns the samples list
        """
        return self.samples    

    def getSampleDescription(self, sample_name):
        """
        Returns the description of a given sample.
        
        """
        return self.sample_description[sample_name]

    def getData(self, sample, gene_name=None, probe_name=None):
        """
        Returns the data value associated with sample, gene or sample, probe 
        """
        # victor: assumes (correctly?) that expression value is the same 
        # whether probe_id or gene_id is used.
        if gene_name is None:
            return self.data_table[self.probe_index[probe_name]][self.sample_index[sample]]
        else:
            return self.data_table[self.gene_index[gene_name]][self.sample_index[sample]]
