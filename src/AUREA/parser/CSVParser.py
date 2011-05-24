class CSVParser:
    """
    Reads a csv file of the format
    ID_REF, IDENTIFIER, SAMP1Name, SAMP2Name, ... ,SAMPnName
    prob1_id, gene1_id, g1S1val, g1S2val, ... , g1Snval
    ...
    probm_id, genem_id, gmS1val, gmS2val, ... , gmSnval 
    """
    def __init__(self, filename, probe_column_name="ID_REF", gene_column_name="IDENTIFIER"):
        self.filename = filename
        self.lock = False
        self.probe_column_name = probe_column_name
        self.gene_column_name = gene_column_name
        f = open(filename, 'r')
        self.raw_content = f.readlines()
        f.close()
        self.getData()

    def getData(s):
        """
        Called automatically by constructor.
        Parses the csv file
        """
        clean = s._clean
        s.column_heading = []
        s.table = []
        s.id_ref_column = None
        s.identifier_column = None
        for line in s.raw_content:
            if len(s.column_heading) == 0:
                s.column_heading = [clean(x) for x in line.strip().split(',')]
            else:
                s.table.append(line.strip().split(','))

    def getTable(self, lock=False):
        """
        Returns the table.
        If you want to operate directly on the table, set lock to True.
        """
        if self.lock:
            raise Exception, "The parser has given up control of the table"
        self.lock = lock
        return self.table

    def getColumnHeadings(self):
        """
        Returns a list of the column headings (the first line of the csv file)
        """
        return self.column_heading

    def getColumnHeadingsInfo(self):
        """
        Not really applicable, but added for compatibility with softparser
        """
        return [(x,x) for x in self.column_heading]

    def getID_REF(self):
        """
        Returns the probe column
        """
        if self.id_ref_column is None:
            clean = self._clean # may have extraneous quotes
            column_heading_index = None
            counter = 0
            for column_heading in self.getColumnHeadings():
                if column_heading == self.probe_column_name:
                    column_heading_index = counter
                counter += 1
            if column_heading_index is None:
                raise Exception, "This CSV file has no ID_REF column, this is required"
            self.id_ref_column = [ clean(row[column_heading_index]) for row in self.table]
        return self.id_ref_column

    def getIDENTIFIER(self):
        """
        This is not guaranteed to be there, but so far it has been.
        If it is not available we will have to handle it somehow.
        Probably just set identifier_label to ID_REF
        This should map to genes and each value will not be unique.
        """
        if self.identifier_column is None:
            clean = self._clean
            column_heading_index = None
            counter = 0
            for column_heading in self.getColumnHeadings():
                if column_heading == self.gene_column_name:
                    column_heading_index = counter
                counter += 1
            if column_heading_index is None:
                raise Exception, "This CSV file has no IDENTIFIER column, set gene_column_name parameter to ID_REF or probe_column_name value if no IDENTIFIER(gene name) is available."
            self.identifier_column = [ clean(row[column_heading_index]) for row in self.table ]
        return self.identifier_column

    def getDataColumnHeadings(self):
        """
        Returns the data column headings
        """
        if self.gene_column_name ==self.probe_column_name:
            return self.getColumnHeadings[1:]
        else:
            return self.getColumnHeadings[2:]

    def getKeyColumnHeadings(self):
        """
        Returns the key column headings
        """
        return [ self.gene_column_name, self.probe_column_name]

    def setProbeColumnName(self,probe_column_name="ID_REF"):
        """
        Sets the name of the probe column.
        """
        self.probe_column_name = probe_column_name

    def setGeneColumnName(self, gene_column_name="IDENTIFIER"):
        """
        Sets the name of the gene column
        """
        self.gene_column_name = gene_column_name

    def _clean(self,val):
        #remove quotes from strings
        if val[0] == '"' or val[0] == "'":
            val = val[1:]
        if val[-1] == '"' or val[-1] == "'":
            val = val[:-1]
        return val
