class SOFTParser:
    """A parser for SOFT formatted datasets GEO SOFT format is documented here:
http://www.ncbi.nlm.nih.gov/projects/geo/info/soft2.html#SOFTformat
Note the docs do not describe everything.
    """
    def __init__(self, filename):
        """
        filename is the name of the file you wish to parse.
        Should handle .soft and .soft.gz
        """
        self.filename = filename
        self.lock = []  #this locks the table if another class has edited it
        if(filename.endswith('.gz')):
            #if its zipped, lets unzip
            import gzip 
            f = gzip.open(filename,'rb')
            self.raw_content = f.readlines()
            f.close()
        else:
            f = open(filename,'r')
            self.raw_content = f.readlines()
            f.close()
        self._getData()


    def _getData(s):
        """
        This is a private helper method that actually breaks the data up into manageable chunks.
        It is the primary worker/parser
        """
        s._initContainers()
        for line in s.raw_content:
            if line[0] == '^': #^ entity indicator
                state = s._addEntity(line)
            elif line[0] == '!': #! entity attribute line
                state = s._addEntityAttribute(line, state)           
            elif line[0] == '#': ## data table header description line
                state = s._addDataTableHeader(line, state)
            elif len(line.strip()) == 0:
                #one file I downloaded(GDS463.soft.gz) had an empty line in it.
                #Just pass if line is empty
                pass
            else: #otherwise, data line
                state = s._addDataLine(line, state)
    
    def _initContainers(s):
        """
        Build the various containers for the SOFTParser object
        """
        s.entities = [] 
        s.column_heading = []
        s.column_heading_info = []
        s.row_heading = []
        s.row_heading_index = []
        s.id_ref_column = None
        s.identifier_column = None
        s.tables = []
     
    def _addEntity(s, line):
        """
        Parses an entity and adds it to the entities list
        """
        ent = line[1:].split('=',1)
        s.entities.append(entity(ent[0].strip(),ent[1].strip()))
        return 1

    def _addEntityAttribute(s, line, curr_state):
        """
        Adds an attribute to the current entity
        """
        state = curr_state
        att = line[1:].split('=',1)
        if(len(att) == 2):
            if att[0].strip() not in s.entities[-1].attributes:
                s.entities[-1].attributes[att[0].strip()] = [att[1].strip()]
            else:
                s.entities[-1].attributes[att[0].strip()].append(att[1].strip())
            state = 2
        return state

    def _addDataTableHeader(s, line, curr_state):
        """
        Parses and stores the data table header description
        """
        state = curr_state

        if state != 3:
            #these get set and created in getRowHeading and setRowHeading
            s.column_heading.append([])
            s.column_heading_info.append([])
        head = line[1:].split('=', 1)
        s.column_heading[-1].append(head[0].strip())
        s.column_heading_info[-1].append((head[0].strip(), head[1].strip()))
        return 3

    def _addDataLine(s, line, curr_state):
        """
        Adds a data line to the table
        """
        state = curr_state
        if state != 4:
            s.lock.append(False)
            s.tables.append([])
        row = line.strip().split('\t') 
        if row != s.column_heading[-1]:#dont add header column
            s.tables[-1].append(row)
        return 4


    def getEntities(self):
        """
        Returns a list of entities
        Entities are meta-data objects.
        they have a type, value and a dict of attributes
        """
        return self.entities

    def getNumTables(self):
        """
        Returns the number of tables in the SOFTParser object
        At this point, this class cannot handle multiple tables, or at least
        I should say that I have not tested it on multiple tables.

        When I find a SOFT file that contains multiple tables I will get it working.
        """        
        return len(self.tables)

    def getTable(self, tableNum=0, lock=False):
        """
        Returns the data table at index tableNum, defaults to the first table
        """
        if self.lock[tableNum]:
            raise Exception, "The parser has given up control of the table"
        self.lock[tableNum] = lock
        return self.tables[tableNum]

    def getColumnHeadings(self, tableNum=0):
        """
        Returns a list of all column headings
        """
        return self.column_heading[tableNum]

    def getColumnHeadingsInfo(self,tableNum = 0):
        """
        Returns a list of tuples containing (column heading, column description)
        """
        return self.column_heading_info[tableNum]

    def setRowHeadings(self, colNum, tableNum=0):
        """
        This lets the user set the column that contains the row classifications.
        In this case that means the gene names.
        """
        raise Exception, "SOFTParser.setRowHeadings is deprecated"
        self.row_heading_index[tableNum] = colNum;

    def getRowHeadings(self, tableNum = 0 ):
        """
        ************DEPRECATED*********************
        use getID_REF and getIDENTIFIER as row labels
This returns list of the row headings in the order they
exist in the table"""
        raise Exception, "SOFTParser.getRowHeadings is deprecated"
        if self.row_heading_index[tableNum] and len(self.row_heading[tableNum]) == 0:
            self.row_heading[tableNum]
            rh_index = self.row_heading_index[tableNum]
            
            for row in self.tables[tableNum]:
                self.row_heading[tableNum].append(row[rh_index])
        elif not self.row_heading_index[tableNum]:
            raise Exception, "You must set the column of the row heading."
        
        return self.row_heading[tableNum]

    def getID_REF(self, id_ref='ID_REF', tableNum=0):
        """
        It appears that this is a required column in SOFT data tables.
        It is required to correspond to the probes.  This in general should be our key
        It will probably be the first column, but we can't really be sure
        This function returns the ordered values of this column for mapping
        back to the rows.
        Each value should be unique
        """
        
        if self.id_ref_column is None:
            column_heading_index = None
            counter = 0
            for column_heading in self.getColumnHeadings():
                if column_heading == id_ref:
                    column_heading_index = counter
                counter += 1
            if column_heading_index is None:
                raise Exception, "This SOFT file has no ID_REF column"
            self.id_ref_column = [ row[column_heading_index] for row in self.tables[tableNum] ]
        return self.id_ref_column

    def getIDENTIFIER(self,identifier_label='IDENTIFIER',tableNum = 0):
        """
        This is not guaranteed to be there, but so far it has been.
        If it is not available we will have to handle it somehow
        This should map to genes and each value will not be unique.
        """
        if self.identifier_column is None:
            column_heading_index = None
            counter = 0
            for column_heading in self.getColumnHeadings():
                if column_heading == identifier_label:
                    column_heading_index = counter
                counter += 1
            if column_heading_index is None:
                raise Exception, "This SOFT file has no IDENTIFIER column"
            self.identifier_column = [ row[column_heading_index] for row in self.tables[tableNum] ]
        return self.identifier_column
 

    def getDataColumnHeadings(self):
        """
        Using the subset entities, this function returns the data column names.
        This is actually the union of the subsets.
        """
        dch = []
        for entity in self.getSubsets():
            for sample in self.getSubsetSamples(entity):
                dch.append(sample)
        return dch
    
    def getKeyColumnHeadings(self):
        """
        Returns any non data column headers.
        i.e. COLUMN_HEADINGS - getDataColumnHeadings()
        """
        dch = self.getDataColumnHeadings()
        kch = []
        for h in self.getColumnHeadings():
             if h not in dch:
                kch.append(h)
        return kch

    def getSubsets(self):
        """
        Returns a list of all entities that are marked as subsets
        """
        subsets = []
        for entity in self.entities:
            if entity.type == 'SUBSET':
                subsets.append(entity)
        return subsets
        
    def getSubsetSamples(self, subset):
        """
        Takes a entity object of type SUBSET
        Returns a list of the subset sample id's found in subset entity 
        """
        samples = subset.attributes['subset_sample_id'][0]
        return [x.strip() for x in samples.split(',')]

    def getNumTables(self):
        """
        Returns the number of tables
        NOTE: I have yet to find a softfile with multiple tables.  This needs to be tested.
        """
        return len(self.tables)

    def printTable(self):
        """
        Helper function.
        """
        for table in self.tables:
            for row in table:
                for value in row:
                    print value,
                    print ",",
                print

    def addEntitiesToDatabase(self, host="localhost", dbName ="SOFTFile", user="AUREA", password="URDumb"):
        """
        A simple entity insertion function.
        This is really a helper function that was used in testing AUREA.
        It needs to be modified if used.
        """
        import psycopg2
        import psycopg2.extensions
        import os.path
        connectstr = "host="+host+" dbname="+dbName+" user="+user+" password="+password
        conn = psycopg2.connect(connectstr)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        c = conn.cursor()
        ref = {'DATABASE':None,'DATASET':None, 'file_name':os.path.basename(self.filename)}
        
        for entity in self.getEntities():
            key, val = entity.addToDatabase(c, **ref)
            if key == 'DATABASE':
                ref[key] = val
            elif key == 'DATASET':
                ref[key] = val
        c.close()
        conn.close()
 
class entity:
    """
    A container for meta-data provided by the soft file.
    Type: the type of entity (Database, subset, etc)
    Value: usually a unique id
    attributes: a dict with related attributes where each key points to a list if provided values
    """
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.attributes = {}

    def addToDatabase(self, cursor, DATABASE=None, DATASET=None, SUBSET=None, file_name=None):
        if self.type == "DATABASE":
            checkQry = "SELECT database_id \
            FROM DATABASE \
            WHERE entity_name = %s"
            val_list = [self.value]
            for key, val in self.attributes.iteritems():
                checkQry += " AND " + key + "= %s"
                
                val_list.append(','.join(val))
            
            cursor.execute(checkQry, tuple(val_list) )
            returnVal = cursor.fetchone()
            if returnVal is None:
                insertQry = "INSERT into database( entity_name "
                insertQry2 = " VALUES (%s "
                for key, val in self.attributes.iteritems():
                    insertQry += ", "+ key
                    insertQry2 += ", %s" 

                cursor.execute(insertQry + ")" + insertQry2 + " ) RETURNING database_id", tuple(val_list))
                returnVal = cursor.fetchone() 
            return ('DATABASE', returnVal[0])
        elif self.type == "DATASET":
            if DATABASE is None:
                raise Exception("Trying to store Dataset without Database")
            chkQry = "SELECT dataset_id FROM dataset WHERE entity_name = %s"
            val_list = [self.value]
            cursor.execute(chkQry, tuple(val_list))
            returnVal = cursor.fetchone()
            if returnVal is None:
                insertQry = "INSERT into dataset(entity_name, database_id, file_name"
                insertQry2 = " VALUES( %s, %s, %s"
                val_list.append(DATABASE)
                val_list.append(file_name)
                
                for key, val in self.attributes.iteritems():
                    insertQry += ", "  + key
                    insertQry2 += ", %s"
                    if key[-5:] == 'count':
                        val_list.append(int(''.join(val)))
                    else:
                        val_list.append(','.join(val))
                qstr =  insertQry + ") " + insertQry2 + ") RETURNING dataset_id;"
                cursor.execute(qstr, tuple(val_list))
                returnVal = cursor.fetchone() 
            return ('DATASET', returnVal[0])
        elif self.type == 'SUBSET':
            ckQry = "SELECT subset_id FROM subset WHERE entity_name = %s and dataset_id = %s"
            val_list = [self.value, DATASET]
            cursor.execute(ckQry, tuple(val_list))
            returnVal = cursor.fetchone()
            if returnVal is None:
                insertQry = "INSERT INTO subset( entity_name, dataset_id"
                insertQry2 = " Values(%s, %s"
                for key, val in self.attributes.iteritems():
                    insertQry += ", " + key
                    insertQry2 += ", %s"
                    if key != 'subset_sample_id':
                        val_list.append(",".join(val))
                    else:
                        val_list.append(val[0].split(','))
                    qstr =  insertQry + ") " + insertQry2 + ")"
                cursor.execute(qstr, tuple(val_list))
            return ('SUBSET', None)
            
        return (None, None)
    def __repr__(self):
        """
        Tag based, called with 'print entity'
        """
        retstr = "<entity type:%s value:%s "%(self.type, self.value)
        for key, value in self.attributes.iteritems():
            retstr += " attributes[%s] : %s"% (key, value)
        retstr += ">"
        return retstr

    def prettyPrint(self):
        """
        Returns a nice human readable description of the entity
        """
        retstr = "%s : %s \n"%(self.type, self.value)
        for key, value in self.attributes.iteritems():
            retstr += "\t %s : %s \n"% (key, ','.join(value))
        return retstr   
import urllib2
import time
import os
import socket
class SOFTDownloader:
    def __init__(self, filename, url="ftp://ftp.ncbi.nih.gov/pub/geo/DATA/SOFT/GDS/", output_directory="data", timeout=30):
        self.timeout = timeout
        file = self.getFile(url, filename)
        if file is not None:
            self.filePath = self.writeFile(file, output_directory, filename)
        else:
            self.filePath = None
    

    def getFile(self, url, filename):
        """
        Note raises urllib2.URLError when it can't find the file
        """
        counter = 0            
        socket.setdefaulttimeout(self.timeout)
        f = urllib2.urlopen(url + filename.strip())
        return f
       
    def writeFile(self, file_obj, dir, filename):
        if os.path.exists(dir):
            fpath = os.path.join(dir, filename)
            local = open(fpath, 'wb')
            local.write(file_obj.read())
            local.close()
            return fpath
        return None

    def getFilePath(self):
        return self.filePath
        
    

if __name__ == "__main__":
    sp = SOFTParser("../data/GDS2545.soft.gz")
    for e in sp.entities:
        print e
        print
    """
    for info in sp.column_heading_info[0]:
        print info[0]
        print info[1]
    sp.printTable()
    for h in     sp.table_headings :
        for key in h.keys():
            print key
            print h[key][0]

    for h in sp.table_headings_ordered:
        for head in h:
            print head
    #sp.printTable()
"""
